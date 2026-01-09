import pytest
from datetime import timedelta
from unittest.mock import AsyncMock
from app.application.services.monitoramento_service import MonitoramentoService
from app.domain.use_cases.calcular_tempo_medio_ordem_servico import CalcularTempoMedioOrdemServico


@pytest.fixture
def mock_ordem_servico_repo():
    return AsyncMock()


@pytest.fixture
def monitoramento_service(mock_ordem_servico_repo):
    return MonitoramentoService(ordem_servico_repo=mock_ordem_servico_repo)


@pytest.mark.asyncio
class TestMonitoramentoService:

    async def test_obter_tempo_medio_retorna_valores(
        self,
        monitoramento_service,
        mock_ordem_servico_repo
    ):
        # Mocka a execução do use case para retornar um timedelta válido
        # 1 dia, 2 horas e 30 minutos
        esperado = timedelta(days=1, hours=2, minutes=30)
        monitoramento_service.use_case.executar = AsyncMock(return_value=esperado)

        resultado = await monitoramento_service.obter_tempo_medio()

        assert resultado.days == 1
        assert resultado.seconds == 2 * 3600 + 30 * 60  # 2 horas + 30 minutos em segundos
        monitoramento_service.use_case.executar.assert_awaited_once()

    async def test_obter_tempo_medio_repassa_excecao(
        self,
        monitoramento_service
    ):
        # Simula exceção no use case
        monitoramento_service.use_case.executar = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(Exception, match="Erro inesperado"):
            await monitoramento_service.obter_tempo_medio()
