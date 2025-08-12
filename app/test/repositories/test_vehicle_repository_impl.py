import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import IntegrityError
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl
from app.domain.entities.vehicle import Vehicle

@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def repo(mock_db):
    return VehicleRepositoryImpl(mock_db)


@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_db):
    vehicle_model = MagicMock(
        id=1,
        license_plate="ABC1234",
        brand="Toyota",
        model="Corolla",
        year=2020,
        client_id=10,
    )
    mock_result = MagicMock()  # resultado sync
    mock_result.scalar_one_or_none.return_value = vehicle_model  # método sync retornando objeto mock
    mock_db.execute.return_value = mock_result  # async function retorna mock_result (não coroutine)

    vehicle = await repo.get_by_id(1)

    mock_db.execute.assert_awaited_once()
    assert vehicle is not None
    assert vehicle.id == vehicle_model.id
    assert vehicle.license_plate == vehicle_model.license_plate


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_db):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    vehicle = await repo.get_by_id(999)

    assert vehicle is None


@pytest.mark.asyncio
async def test_get_by_plate_found(repo, mock_db):
    vehicle_model = MagicMock(
        id=2,
        license_plate="XYZ9876",
        brand="Honda",
        model="Civic",
        year=2019,
        client_id=20,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = vehicle_model
    mock_db.execute.return_value = mock_result

    vehicle = await repo.get_by_plate("XYZ9876")

    assert vehicle is not None
    assert vehicle.license_plate == "XYZ9876"


@pytest.mark.asyncio
async def test_list_all(repo, mock_db):
    vehicle_models = [
        MagicMock(id=1, license_plate="A1", brand="B1", model="M1", year=2000, client_id=1),
        MagicMock(id=2, license_plate="A2", brand="B2", model="M2", year=2001, client_id=2),
    ]
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = vehicle_models
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    vehicles = await repo.list_all()

    assert len(vehicles) == 2
    assert vehicles[0].id == 1
    assert vehicles[1].license_plate == "A2"



@pytest.mark.asyncio
async def test_create_success(repo, mock_db):
    vehicle = Vehicle(
        id=None,
        license_plate="NEW1234",
        brand="Ford",
        model="Focus",
        year=2021,
        client_id=30,
    )

    vehicle_model = MagicMock(
        id=10,
        license_plate="NEW1234",
        brand="Ford",
        model="Focus",
        year=2021,
        client_id=30,
    )
    # Simula add, commit e refresh
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    # Depois do refresh o id é setado no model
    def refresh_side_effect(vm):
        vm.id = 10
    mock_db.refresh.side_effect = refresh_side_effect

    with patch("app.infrastructure.repositories.vehicle_repository_impl.VehicleModel", return_value=vehicle_model):
        created = await repo.create(vehicle)

    assert created.id == 10
    assert created.license_plate == vehicle.license_plate


@pytest.mark.asyncio
async def test_create_integrity_error(repo, mock_db):
    vehicle = Vehicle(
        id=None,
        license_plate="DUPLICATE",
        brand="Brand",
        model="Model",
        year=2020,
        client_id=1,
    )

    mock_db.add.return_value = None
    mock_db.commit.side_effect = IntegrityError("duplicate key", params=None, orig=None)
    mock_db.rollback.return_value = None

    with pytest.raises(IntegrityError):
        await repo.create(vehicle)
    mock_db.rollback.assert_awaited()


@pytest.mark.asyncio
async def test_update_success(repo, mock_db):
    vehicle = Vehicle(
        id=1,
        license_plate="UPDATED",
        brand="BrandU",
        model="ModelU",
        year=2022,
        client_id=99,
    )

    vehicle_model = MagicMock(
        id=1,
        license_plate="OLD",
        brand="OldBrand",
        model="OldModel",
        year=2020,
        client_id=50,
    )

    mock_db.get.return_value = vehicle_model
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    updated = await repo.update(vehicle)

    assert updated.id == vehicle_model.id
    assert vehicle_model.license_plate == "UPDATED"
    assert vehicle_model.brand == "BrandU"
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()


@pytest.mark.asyncio
async def test_update_not_found(repo, mock_db):
    vehicle = Vehicle(
        id=999,
        license_plate="NOTFOUND",
        brand="None",
        model="None",
        year=2000,
        client_id=0,
    )

    mock_db.get.return_value = None

    updated = await repo.update(vehicle)
    assert updated is None


@pytest.mark.asyncio
async def test_delete_found(repo, mock_db):
    vehicle_model = MagicMock()
    mock_db.get.return_value = vehicle_model
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    await repo.delete(1)

    mock_db.delete.assert_awaited_with(vehicle_model)
    mock_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_delete_not_found(repo, mock_db):
    mock_db.get.return_value = None

    await repo.delete(999)

    mock_db.delete.assert_not_awaited()
    mock_db.commit.assert_not_awaited()
