import pytest
import pytest_asyncio
from fastapi import status
from unittest.mock import AsyncMock, patch
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.fast_api import create_app
from app.infrastructure.auth_dependencies import get_current_user
from passlib.context import CryptContext
from app.infrastructure.auth import verify_password

@pytest.fixture(scope="function")
def app():
    app = create_app()
    yield app

@pytest_asyncio.fixture(scope="function")
async def async_client(app):
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="function")
def mock_user():
    hashed_password = pwd_context.hash("correct_password")
    return UserEntity(
        uid="1",
        nome="Admin Test",
        email="admin@test.com",
        hashed_password=hashed_password,
        funcao=UserFuncao.ADMIN,
    )

@pytest.fixture(scope="function")
def mock_user_service(mock_user):
    mock = AsyncMock()

    async def get_user_by_email(email):
        return mock_user if email == "admin@test.com" else None

    mock.get_user_by_email.side_effect = get_user_by_email
    return mock

@pytest.fixture(scope="function")
def override_services(app, mock_user_service):
    app.container.user_service.override(mock_user_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.user_service.reset_override()
    app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestAuthAPI:

    async def test_login_success(self, async_client, override_services, mock_user_service, mock_user):
        async def get_user_by_email(email):
            return mock_user if email == "admin@test.com" else None

        mock_user_service.get_user_by_email.side_effect = get_user_by_email

        with patch("app.infrastructure.auth.verify_password", return_value=True):
            response = await async_client.post(
                "/auth/token",
                data={"username": "admin@test.com", "password": "correct_password"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_invalid_password(self, async_client, override_services, mock_user_service, mock_user):
        async def get_user_by_email(email):
            return mock_user if email == "admin@test.com" else None

        mock_user_service.get_user_by_email.side_effect = get_user_by_email

        with patch("app.infrastructure.auth.verify_password", return_value=False):
            response = await async_client.post(
                "/auth/token",
                data={"username": "admin@test.com", "password": "wrong_password"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert data["detail"] == "Email ou senha inválidos"

    async def test_login_user_not_found(self, async_client, override_services, mock_user_service):
        async def get_user_by_email(email):
            return None

        mock_user_service.get_user_by_email.side_effect = get_user_by_email

        response = await async_client.post(
            "/auth/token",
            data={"username": "unknown@test.com", "password": "any_password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert data["detail"] == "Email ou senha inválidos"
