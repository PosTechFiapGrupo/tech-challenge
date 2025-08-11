import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.infrastructure.container import Container


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_user_service():
    return AsyncMock()


class TestUserAPI:

    def test_get_all_users_empty(self, client, mock_user_service):
        # Mock para retornar lista vazia
        mock_user_service.get_all_users.return_value = []

        with client.app.container.user_service.override(mock_user_service):
            response = client.get("/users/")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_user_success(self, client, mock_user_service):
        user_data = {
            "nome": "Marta Souza",
            "email": "marta@example.com",
            "password": "senhaSegura123",
            "funcao": "cliente"
        }

        from app.domain.entities.user import UserEntity, UserFuncao

        mock_user = UserEntity(
            "1", "Marta Souza", "marta@example.com", "hashed_senhaSegura123", UserFuncao.CLIENTE
        )

        # Mock get_user_by_email para simular que email não existe
        mock_user_service.get_user_by_email.return_value = None

        # Mock async create_user para retornar o mock_user
        async def fake_create_user(user_entity, plain_password):
            return mock_user

        mock_user_service.create_user.side_effect = fake_create_user

        with client.app.container.user_service.override(mock_user_service):
            response = client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Marta Souza"
        assert data["email"] == "marta@example.com"

    def test_create_user_invalid_email(self, client):
        user_data = {
            "nome": "Marta Souza",
            "email": "email-invalido",
            "password": "senhaSegura123",
            "funcao": "cliente"
        }

        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Ajuste para 400 conforme validação de email

    def test_get_user_by_id_not_found(self, client, mock_user_service):
        mock_user_service.get_user_by_id.return_value = None

        with client.app.container.user_service.override(mock_user_service):
            response = client.get("/users/999")

        assert response.status_code == 404
