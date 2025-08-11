import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.domain.entities.cliente import ClienteEntity
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.fast_api import create_app
from app.infrastructure.auth_dependencies import get_current_user


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
def mock_cliente_service():
    mock = AsyncMock()

    async def fake_create_cliente(cliente_entity):
        return cliente_entity

    mock.create_cliente.side_effect = fake_create_cliente
    mock.get_all_clientes.return_value = []
    mock.get_cliente_by_id.return_value = None

    return mock


@pytest.fixture(scope="function")
def override_services(app, mock_cliente_service, mock_user_service, mock_password_service):
    app.container.cliente_service.override(mock_cliente_service)
    app.container.user_service.override(mock_user_service)
    app.container.password_service.override(mock_password_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.cliente_service.reset_override()
    app.container.user_service.reset_override()
    app.container.password_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestClienteAPI:

    async def test_get_all_clientes_empty(self, async_client, override_services, mock_cliente_service):
        mock_cliente_service.get_all_clientes.return_value = []

        response = await async_client.get("/clientes/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_cliente_success(self, async_client, override_services):
        cliente_data = {
            "nome": "João Silva",
            "telefone": "11999999999",
            "email": "joao@email.com",
            "cpf": "12345678901",
        }

        response = await async_client.post("/clientes/", json=cliente_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@email.com"

    async def test_create_cliente_invalid_email(self, async_client, override_services):
        cliente_data = {
            "nome": "João Silva",
            "telefone": "11999999999",
            "email": "invalid-email",
            "cpf": "12345678901",
        }

        response = await async_client.post("/clientes/", json=cliente_data)
        assert response.status_code == 422  # erro de validação

    async def test_get_cliente_by_id_not_found(self, async_client, override_services, mock_cliente_service):
        mock_cliente_service.get_cliente_by_id.return_value = None

        response = await async_client.get("/clientes/999")
        assert response.status_code == 404
