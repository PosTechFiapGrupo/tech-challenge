import pytest
from unittest.mock import AsyncMock, Mock
from app.application.services.ordem_servico import OrdemServicoService
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from app.infrastructure.schemas.ordem_servico import OrdemServicoUpdate


@pytest.fixture
def mock_use_case():
    return AsyncMock()


@pytest.fixture
def mock_cliente_validator():
    validator = AsyncMock()
    validator.validate_exists = AsyncMock()
    return validator


@pytest.fixture
def mock_servico_validator():
    validator = AsyncMock()
    validator.validate_exists = AsyncMock()
    return validator


@pytest.fixture
def mock_vehicle_validator():
    validator = AsyncMock()
    validator.validate_exists = AsyncMock()
    return validator


@pytest.fixture
def mock_ordem_servico_validator():
    return Mock()


@pytest.fixture
def ordem_servico_service(
    mock_use_case,
    mock_cliente_validator,
    mock_vehicle_validator,
    mock_servico_validator,
    mock_ordem_servico_validator,
):
    return OrdemServicoService(
        use_case=mock_use_case,
        cliente_validator=mock_cliente_validator,
        vehicle_validator=mock_vehicle_validator,
        servico_validator=mock_servico_validator,
        ordem_servico_validator=mock_ordem_servico_validator,
    )


@pytest.fixture
def sample_os():
    return OrdemServicoEntity(
        uid="1",
        cliente_id="123",
        vehicle_id="456",
        servico_ids=["1", "2"],
        status=StatusOrdemServico.RECEBIDA,
    )


@pytest.mark.asyncio
async def test_criar_ordem_servico(
    ordem_servico_service,
    sample_os,
    mock_use_case,
    mock_cliente_validator,
    mock_vehicle_validator,
    mock_servico_validator,
):
    mock_use_case.create_ordem_servico.return_value = sample_os

    result = await ordem_servico_service.criar_ordem_servico(sample_os)

    assert result == sample_os
    mock_cliente_validator.validate_exists.assert_called_once_with("123")
    mock_vehicle_validator.validate_exists.assert_called_once_with("456")
    assert mock_servico_validator.validate_exists.call_count == 2
    mock_use_case.create_ordem_servico.assert_called_once_with(sample_os)


@pytest.mark.asyncio
async def test_listar_ordens_servico(ordem_servico_service, mock_use_case, sample_os):
    mock_use_case.get_all_ordens_servico.return_value = [sample_os]

    result = await ordem_servico_service.listar_ordens_servico()

    assert result == [sample_os]
    mock_use_case.get_all_ordens_servico.assert_called_once()


@pytest.mark.asyncio
async def test_buscar_ordem_servico_por_id(
    ordem_servico_service, mock_use_case, sample_os
):
    mock_use_case.get_ordem_servico_by_id.return_value = sample_os

    result = await ordem_servico_service.buscar_ordem_servico_por_id("1")

    assert result == sample_os
    mock_use_case.get_ordem_servico_by_id.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_atualizar_ordem_servico(ordem_servico_service, mock_use_case, sample_os):
    update_data = OrdemServicoUpdate(status=StatusOrdemServico.FINALIZADA)
    mock_use_case.get_ordem_servico_by_id.return_value = sample_os
    mock_use_case.update_ordem_servico.return_value = sample_os

    result = await ordem_servico_service.atualizar_ordem_servico("1", update_data)

    assert result == sample_os
    assert sample_os.status == StatusOrdemServico.FINALIZADA
    mock_use_case.get_ordem_servico_by_id.assert_called_once_with("1")
    mock_use_case.update_ordem_servico.assert_called_once_with(sample_os)


@pytest.mark.asyncio
async def test_atualizar_ordem_servico_not_found(ordem_servico_service, mock_use_case):
    mock_use_case.get_ordem_servico_by_id.return_value = None

    with pytest.raises(ValueError, match="Ordem de serviço não encontrada"):
        await ordem_servico_service.atualizar_ordem_servico("1", OrdemServicoUpdate())