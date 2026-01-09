from datetime import timedelta
from typing import Dict, Optional

import newrelic.agent
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.services.monitoramento_service import MonitoramentoService
from app.infrastructure.auth_dependencies import role_required
from app.infrastructure.logging_config import get_logger
from app.infrastructure.repositories.ordem_servico_impl import OrdemServicoRepositoryImpl
from app.infrastructure.schemas.monitoramento_schema import TempoMedioServicosOut

logger = get_logger(__name__)

router = APIRouter(prefix="/monitoramento", tags=["Monitoramento"])


class MetricasCompletasOut(BaseModel):
    """Schema de saída para métricas completas de monitoramento."""
    tempo_medio_total: Optional[Dict] = None
    contagem_por_status: Dict[str, int] = {}
    volume_hoje: int = 0


class TempoMedioPorStatusOut(BaseModel):
    """Schema de saída para tempo médio por status."""
    recebida: Dict = {}
    em_diagnostico: Dict = {}
    aguardando_aprovacao: Dict = {}
    em_execucao: Dict = {}
    finalizada: Dict = {}
    cancelada: Dict = {}


def format_timedelta(td: timedelta) -> str:
    total_segundos = int(td.total_seconds())
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{dias} dias, {horas} horas, {minutos} minutos"


@router.get(
    "/tempo-medio-servicos",
    response_model=TempoMedioServicosOut,
    dependencies=[Depends(role_required("admin", "atendente"))],
    summary="Tempo médio de execução das ordens de serviço",
    description="Retorna o tempo médio desde a abertura até o fechamento das ordens de serviço finalizadas."
)
async def tempo_medio_servicos():
    """
    Calcula o tempo médio de execução de ordens de serviço.
    
    Usado para dashboard de monitoramento:
    - Tempo médio de execução geral
    - Identificar tendências de performance
    """
    repo = OrdemServicoRepositoryImpl()
    service = MonitoramentoService(repo)
    tempo_medio = await service.obter_tempo_medio()
    
    if tempo_medio is None:
        raise HTTPException(status_code=404, detail="Nenhum serviço finalizado")

    total_segundos = int(tempo_medio.total_seconds())
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)

    logger.info(
        "Tempo médio de serviços consultado",
        extra={
            "dias": dias,
            "horas": horas,
            "minutos": minutos,
            "total_segundos": total_segundos,
        }
    )

    return TempoMedioServicosOut(
        dias=dias,
        horas=horas,
        minutos=minutos,
    )


@router.get(
    "/metricas",
    response_model=MetricasCompletasOut,
    dependencies=[Depends(role_required("admin", "atendente"))],
    summary="Métricas completas de ordens de serviço",
    description="Retorna métricas completas incluindo volume diário, contagem por status e tempo médio."
)
async def metricas_completas():
    """
    Retorna métricas completas para dashboards do New Relic.
    
    Inclui:
    - Volume de ordens de serviço criadas hoje
    - Contagem de ordens por status
    - Tempo médio de execução
    """
    repo = OrdemServicoRepositoryImpl()
    service = MonitoramentoService(repo)
    
    try:
        metricas = await service.obter_metricas_completas()
        
        logger.info(
            "Métricas completas consultadas",
            extra={
                "volume_hoje": metricas.get("volume_hoje", 0),
                "contagem_por_status": metricas.get("contagem_por_status", {}),
            }
        )
        
        return MetricasCompletasOut(**metricas)
    
    except Exception as e:
        logger.error(
            "Erro ao obter métricas completas",
            extra={"error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao calcular métricas"
        )


@router.get(
    "/tempo-por-status",
    response_model=TempoMedioPorStatusOut,
    dependencies=[Depends(role_required("admin", "atendente"))],
    summary="Tempo médio por status",
    description="Retorna o tempo médio que as ordens permanecem em cada status."
)
async def tempo_medio_por_status():
    """
    Calcula tempo médio que as OS permanecem em cada status.
    
    Útil para identificar gargalos no processo:
    - Diagnóstico demorado → Falta de mecânicos
    - Aprovação lenta → Problema de comunicação com cliente
    - Execução longa → Complexidade do serviço
    """
    repo = OrdemServicoRepositoryImpl()
    service = MonitoramentoService(repo)
    
    tempos = await service.obter_tempo_medio_por_status()
    
    logger.info(
        "Tempo por status consultado",
        extra={"tempos": tempos}
    )
    
    return TempoMedioPorStatusOut(**tempos)


@router.get(
    "/health-metrics",
    dependencies=[Depends(role_required("admin"))],
    summary="Métricas de saúde da aplicação",
    description="Retorna métricas de saúde e performance da aplicação."
)
async def health_metrics():
    """Endpoint para métricas de saúde da aplicação."""
    try:
        linking_metadata = newrelic.agent.get_linking_metadata() or {}
        return {
            "status": "healthy",
            "newrelic": {
                "entity_name": linking_metadata.get("entity.name", ""),
                "entity_type": linking_metadata.get("entity.type", ""),
                "hostname": linking_metadata.get("hostname", ""),
            }
        }
    except Exception:
        return {"status": "healthy", "newrelic": {"status": "not_available"}}