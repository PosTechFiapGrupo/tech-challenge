from datetime import date, timedelta
from typing import Optional

import newrelic.agent

from app.domain.entities.status_ordem_servico import StatusOrdemServico
from app.domain.use_cases.calcular_tempo_medio_ordem_servico import CalcularTempoMedioOrdemServico
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class MonitoramentoService:
    """
    Serviço de monitoramento e métricas para ordens de serviço.
    
    Fornece dados para dashboards do New Relic:
    - Volume diário de ordens de serviço
    - Tempo médio de execução por status
    - Contagens por status
    """
    
    def __init__(self, ordem_servico_repo):
        self.ordem_servico_repo = ordem_servico_repo
        self.use_case = CalcularTempoMedioOrdemServico(ordem_servico_repo)

    async def obter_tempo_medio(self) -> Optional[timedelta]:
        """Calcula tempo médio de execução de todas as OS finalizadas."""
        tempo = await self.use_case.executar()
        self._record_tempo_medio_metric(tempo)
        return tempo

    async def obter_metricas_completas(self) -> dict:
        """
        Obtém métricas completas de ordens de serviço para dashboards.
        
        Retorna:
            - tempo_medio_total: Tempo médio geral de execução
            - contagem_por_status: Quantidade de OS por status
            - volume_diario: Contagem de OS criadas hoje
        """
        metricas = {
            "tempo_medio_total": None,
            "contagem_por_status": {},
            "volume_hoje": 0,
        }
        
        try:
            # Tempo médio geral
            tempo_medio = await self.use_case.executar()
            if tempo_medio:
                metricas["tempo_medio_total"] = {
                    "total_seconds": tempo_medio.total_seconds(),
                    "formatted": self._format_timedelta(tempo_medio)
                }
            
            # Contagem por status
            all_ordens = await self.ordem_servico_repo.get_all()
            
            for status in StatusOrdemServico:
                count = len([os for os in all_ordens if os.status == status])
                metricas["contagem_por_status"][status.value] = count
                self._record_status_count_metric(status.value, count)
            
            hoje = date.today()
            volume_hoje = len([
                os for os in all_ordens 
                if os.data_abertura and os.data_abertura.date() == hoje
            ])
            metricas["volume_hoje"] = volume_hoje
            self._record_volume_metric(volume_hoje)
            
            logger.info(
                "Métricas de monitoramento calculadas",
                extra={
                    "volume_hoje": volume_hoje,
                    "total_ordens": len(all_ordens),
                }
            )
            
        except Exception as e:
            logger.error(
                "Erro ao calcular métricas de monitoramento",
                extra={"error": str(e)},
                exc_info=True
            )
            raise
        
        return metricas

    async def obter_tempo_medio_por_status(self) -> dict:
        """
        Calcula tempo médio que as OS permanecem em cada status.
        
        Útil para identificar gargalos no processo:
        - Diagnóstico demorado
        - Execução lenta
        - Aprovação pendente
        """
        # TODO: Implementar quando houver tabela de histórico de status
        # Por enquanto retorna dados mock para estruturar o dashboard
        return {
            "recebida": {"avg_hours": 0, "count": 0},
            "em_diagnostico": {"avg_hours": 0, "count": 0},
            "aguardando_aprovacao": {"avg_hours": 0, "count": 0},
            "em_execucao": {"avg_hours": 0, "count": 0},
            "finalizada": {"avg_hours": 0, "count": 0},
            "cancelada": {"avg_hours": 0, "count": 0},
        }

    def _format_timedelta(self, td: timedelta) -> str:
        """Formata timedelta para string legível."""
        total_segundos = int(td.total_seconds())
        dias, resto = divmod(total_segundos, 86400)
        horas, resto = divmod(resto, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{dias}d {horas}h {minutos}m"

    def _record_tempo_medio_metric(self, tempo: Optional[timedelta]) -> None:
        """Registra métrica de tempo médio no New Relic."""
        if not tempo:
            return
        self._record_metric("Custom/OrdemServico/TempoMedioExecucao", tempo.total_seconds())

    def _record_status_count_metric(self, status: str, count: int) -> None:
        """Registra contagem por status no New Relic."""
        self._record_metric(f"Custom/OrdemServico/CountByStatus/{status}", count)

    def _record_volume_metric(self, count: int) -> None:
        """Registra volume diário no New Relic."""
        self._record_metric("Custom/OrdemServico/VolumeHoje", count)

    def _record_metric(self, name: str, value: float) -> None:
        """Helper para registrar métrica no New Relic."""
        try:
            newrelic.agent.record_custom_metric(name, value)
        except Exception:
            pass
            pass
