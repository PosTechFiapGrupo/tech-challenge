import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.domain.entities.servico import ServicoEntity
from app.domain.entities.user import UserEntity, UserFuncao
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
def mock_servico_service():
    mock = AsyncMock()
    mock.get_all_servicos = AsyncMock()
    mock.create_servico = AsyncMock()
    mock.get_servico_by_id = AsyncMock()
    return mock


@pytest.fixture(scope="function")
def override_services(app, mock_servico_service, mock_user_service, mock_password_service):
    app.container.servico_service.override(mock_servico_service)
    app.container.user_service.override(mock_user_service)
    app.container.password_service.override(mock_password_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.servico_service.reset_override()
    app.container.user_service.reset_override()
    app.container.password_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestServicoAPI:

    async def test_get_all_servicos_empty(self, async_client, override_services, mock_servico_service):
        mock_servico_service.get_all_servicos.return_value = []

        response = await async_client.get("/servicos/")

        assert response.status_code == 200
        assert response.json() == []

    async def test_create_servico_success(self, async_client, override_services, mock_servico_service):
        servico_data = {"descricao": "Consultoria em TI", "preco": 150.00}

        mock_servico = ServicoEntity("1", "Consultoria em TI", 150.00)
        mock_servico_service.create_servico.return_value = mock_servico

        response = await async_client.post("/servicos/", json=servico_data)

        assert response.status_code == 201
        data = response.json()
        assert data["descricao"] == "Consultoria em TI"
        assert data["preco"] == 150.00

    async def test_create_servico_invalid_price(self, async_client, override_services):
        servico_data = {"descricao": "Consultoria em TI", "preco": -50.00}

        response = await async_client.post("/servicos/", json=servico_data)

        assert response.status_code == 422  # Validation error

    async def test_get_servico_by_id_not_found(self, async_client, override_services, mock_servico_service):
        mock_servico_service.get_servico_by_id.return_value = None

        response = await async_client.get("/servicos/999")

        assert response.status_code == 404
