import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, AsyncMock, patch
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
def mock_user_service(mock_user):
    mock = AsyncMock()

    async def get_user_by_email(email):
        return mock_user if email == "admin@test.com" else None

    async def get_user_by_id(user_id):
        return mock_user if user_id == "1" else None

    async def fake_create_user(user_entity, plain_password):
        # Retorna o user_entity passado para simular a criação real
        return user_entity

    mock.get_user_by_email.side_effect = get_user_by_email
    mock.get_user_by_id.side_effect = get_user_by_id
    mock.create_user.side_effect = fake_create_user

    return mock


@pytest.fixture(scope="function")
def override_services(app, mock_user_service):
    # Override user_service no container
    app.container.user_service.override(mock_user_service)

    # Mocka o get_current_user para sempre retornar o mock_user
    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    # Limpa overrides
    app.container.user_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestUserAPI:

    async def test_get_all_users_empty(self, async_client, override_services, mock_user_service):
        mock_user_service.get_all_users.return_value = []

        response = await async_client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_user_success(self, async_client, override_services):
        user_data = {
            "nome": "Marta Souza",
            "email": "marta@example.com",
            "password": "senhaSegura123",
            "funcao": "admin"
        }

        response = await async_client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Marta Souza"
        assert data["email"] == "marta@example.com"

    async def test_create_user_invalid_email(self, async_client, override_services):
        user_data = {
            "nome": "Marta Souza",
            "email": "email-invalido",
            "password": "senhaSegura123",
            "funcao": "admin"
        }

        response = await async_client.post("/users/", json=user_data)
        assert response.status_code == 422

    async def test_get_user_by_id_not_found(self, async_client, override_services, mock_user_service):
        mock_user_service.get_user_by_id.return_value = None

        response = await async_client.get("/users/999")
        assert response.status_code == 404
