import pytest
from unittest.mock import AsyncMock
from app.domain.entities.vehicle import Vehicle
from app.application.services.vehicle import VehicleService

@pytest.fixture
def mock_use_case():
    return AsyncMock()

@pytest.fixture
def mock_veiculo_validator():
    validator = AsyncMock()
    validator.validate_exists = AsyncMock()
    return validator

@pytest.fixture
def vehicle_service(mock_use_case, mock_veiculo_validator):
    return VehicleService(
        use_case=mock_use_case,
        vehicle_validator=mock_veiculo_validator
    )

@pytest.fixture
def sample_vehicle():
    return Vehicle(
        id=1,
        license_plate="ABC1D23",
        model="TestModel",
        brand="TestBrand",
        year=2020
    )

@pytest.mark.asyncio
async def test_criar_vehicle(vehicle_service, mock_use_case, sample_vehicle):
    mock_use_case.create.return_value = sample_vehicle

    result = await vehicle_service.criar_vehicle(sample_vehicle)

    assert result == sample_vehicle
    mock_use_case.create.assert_called_once_with(sample_vehicle)

@pytest.mark.asyncio
async def test_listar_vehicles(vehicle_service, mock_use_case, sample_vehicle):
    mock_use_case.list.return_value = [sample_vehicle]

    result = await vehicle_service.listar_vehicles()

    assert result == [sample_vehicle]
    mock_use_case.list.assert_called_once()

@pytest.mark.asyncio
async def test_buscar_vehicle_por_id(vehicle_service, mock_use_case, sample_vehicle):
    mock_use_case.get.return_value = sample_vehicle

    result = await vehicle_service.buscar_vehicle_por_id(1)

    assert result == sample_vehicle
    mock_use_case.get.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_atualizar_vehicle(vehicle_service, mock_use_case, sample_vehicle):
    mock_use_case.update.return_value = sample_vehicle

    result = await vehicle_service.atualizar_vehicle(sample_vehicle)

    assert result == sample_vehicle
    mock_use_case.update.assert_called_once_with(sample_vehicle)

@pytest.mark.asyncio
async def test_deletar_vehicle(vehicle_service, mock_use_case):
    mock_use_case.delete.return_value = None

    await vehicle_service.deletar_vehicle(1)

    mock_use_case.delete.assert_called_once_with(1)