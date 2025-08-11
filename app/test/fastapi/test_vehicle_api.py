import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.domain.entities.vehicle import Vehicle
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.auth_dependencies import get_current_user
from app.domain.exceptions import EntityAlreadyExists, EntityNotFound


@pytest.fixture(scope="function")
def app():
    app = create_app()
    yield app


@pytest_asyncio.fixture(scope="function")
async def async_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_user():
    return UserEntity(
        uid="1",
        nome="Admin Test",
        email="admin@test.com",
        hashed_password="fakehashedpassword",
        funcao=UserFuncao.ADMIN,
    )


@pytest.fixture(scope="function")
def mock_password_service():
    mock = AsyncMock()
    mock.verify_password.return_value = True
    mock.hash_password.return_value = "fakehashedpassword"
    return mock


@pytest.fixture(scope="function")
def mock_user_service(mock_user, mock_password_service):
    mock = AsyncMock()

    async def get_user_by_email(email):
        return mock_user if email == "admin@test.com" else None

    async def get_user_by_id(user_id):
        return mock_user if user_id == "1" else None

    async def fake_create_user(user_entity, plain_password):
        return user_entity

    mock.get_user_by_email.side_effect = get_user_by_email
    mock.get_user_by_id.side_effect = get_user_by_id
    mock.create_user.side_effect = fake_create_user
    mock.password_service = mock_password_service

    return mock


@pytest.fixture(scope="function")
def mock_vehicle_service():
    mock = AsyncMock()
    mock.criar_vehicle = AsyncMock()
    mock.buscar_vehicle_por_id = AsyncMock()
    mock.listar_vehicles = AsyncMock()
    mock.atualizar_vehicle = AsyncMock()
    mock.deletar_vehicle = AsyncMock()
    return mock


@pytest.fixture(scope="function")
def vehicle_data():
    return {
        "license_plate": "ABC1D23",
        "model": "TestModel",
        "brand": "TestBrand",
        "year": 2020,
    }


@pytest.fixture(scope="function")
def override_services(app, mock_vehicle_service, mock_user_service, mock_password_service):
    app.container.vehicle_service.override(mock_vehicle_service)
    app.container.user_service.override(mock_user_service)
    app.container.password_service.override(mock_password_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.vehicle_service.reset_override()
    app.container.user_service.reset_override()
    app.container.password_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestVehicleAPI:

    async def test_create_vehicle_success(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        from app.infrastructure.handlers import vehicle_handler
        vehicle_handler.validate_vehicle_plate = lambda _: True  # placa válida

        mock_vehicle_service.criar_vehicle.return_value = Vehicle(id=1, **vehicle_data)

        response = await async_client.post("/vehicles/", json=vehicle_data)

        assert response.status_code == 200
        data = response.json()
        assert data["license_plate"] == vehicle_data["license_plate"]

    async def test_create_vehicle_invalid_plate(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        from app.infrastructure.handlers import vehicle_handler
        vehicle_handler.validate_vehicle_plate = lambda _: False  # placa inválida

        response = await async_client.post("/vehicles/", json=vehicle_data)

        assert response.status_code == 400
        assert "placa" in response.json()["detail"].lower()

    async def test_create_vehicle_duplicate(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        from app.infrastructure.handlers import vehicle_handler
        vehicle_handler.validate_vehicle_plate = lambda _: True  # placa válida para permitir ir ao erro de duplicação

        mock_vehicle_service.criar_vehicle.side_effect = EntityAlreadyExists("já cadastrada")

        response = await async_client.post("/vehicles/", json=vehicle_data)

        assert response.status_code == 400
        assert "já cadastrada" in response.json()["detail"].lower()

    async def test_get_vehicle_success(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        mock_vehicle_service.buscar_vehicle_por_id.return_value = Vehicle(id=1, **vehicle_data)

        response = await async_client.get("/vehicles/1")

        assert response.status_code == 200
        data = response.json()
        assert data["license_plate"] == vehicle_data["license_plate"]

    async def test_get_vehicle_not_found(self, async_client, override_services, mock_vehicle_service):
        mock_vehicle_service.buscar_vehicle_por_id.side_effect = EntityNotFound("veículo não encontrado")

        response = await async_client.get("/vehicles/999")

        assert response.status_code == 404
        assert "veículo não encontrado" in response.json()["detail"].lower()

    async def test_list_vehicles(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        mock_vehicle_service.listar_vehicles.return_value = [Vehicle(id=1, **vehicle_data)]

        response = await async_client.get("/vehicles/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_update_vehicle_success(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        mock_vehicle_service.atualizar_vehicle.return_value = Vehicle(id=1, **vehicle_data)
        vehicle_data_with_id = {"id": 1, **vehicle_data}

        response = await async_client.put("/vehicles/", json=vehicle_data_with_id)

        assert response.status_code == 200

    async def test_update_vehicle_not_found(self, async_client, override_services, mock_vehicle_service, vehicle_data):
        mock_vehicle_service.atualizar_vehicle.return_value = None
        vehicle_data_with_id = {"id": 1, **vehicle_data}

        response = await async_client.put("/vehicles/", json=vehicle_data_with_id)

        assert response.status_code == 404
        assert "vehicle not found" in response.json()["detail"].lower()

    async def test_delete_vehicle(self, async_client, override_services, mock_vehicle_service):
        mock_vehicle_service.deletar_vehicle.return_value = None

        response = await async_client.delete("/vehicles/1")

        assert response.status_code == 204
