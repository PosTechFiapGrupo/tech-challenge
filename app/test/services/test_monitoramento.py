import pytest
from unittest.mock import AsyncMock
from app.application.services.monitoramento_service import MonitoramentoService
from app.domain.use_cases.calcular_tempo_medio_ordem_servico import CalcularTempoMedioOrdemServico
from app.infrastructure.schemas.monitoramento_schema import TempoMedioServicosOut


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
        # Mocka a execução do use case para retornar um objeto válido
        esperado = TempoMedioServicosOut(dias=1, horas=2, minutos=30)
        monitoramento_service.use_case.executar = AsyncMock(return_value=esperado)

        resultado = await monitoramento_service.obter_tempo_medio()

        assert resultado.dias == 1
        assert resultado.horas == 2
        assert resultado.minutos == 30
        monitoramento_service.use_case.executar.assert_awaited_once()

    async def test_obter_tempo_medio_repassa_excecao(
        self,
        monitoramento_service
    ):
        # Simula exceção no use case
        monitoramento_service.use_case.executar = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(Exception, match="Erro inesperado"):
            await monitoramento_service.obter_tempo_medio()
