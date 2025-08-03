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
def mock_cliente_service():
    return AsyncMock()


class TestClienteAPI:

    def test_get_all_clientes_empty(self, client, mock_cliente_service):
        # Mock the service to return empty list
        mock_cliente_service.get_all_clientes.return_value = []

        with client.app.container.cliente_service.override(mock_cliente_service):
            response = client.get("/clientes/")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_cliente_success(self, client, mock_cliente_service):
        cliente_data = {
            "nome": "João Silva",
            "telefone": "11999999999",
            "email": "joao@email.com",
            "cpf": "12345678901",
        }

        from app.domain.entities.cliente import ClienteEntity

        mock_cliente = ClienteEntity(
            "1", "João Silva", "11999999999", "joao@email.com", "12345678901"
        )
        mock_cliente_service.create_cliente.return_value = mock_cliente

        with client.app.container.cliente_service.override(mock_cliente_service):
            response = client.post("/clientes/", json=cliente_data)

        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@email.com"

    def test_create_cliente_invalid_email(self, client):
        cliente_data = {
            "nome": "João Silva",
            "telefone": "11999999999",
            "email": "invalid-email",
            "cpf": "12345678901",
        }

        response = client.post("/clientes/", json=cliente_data)
        assert response.status_code == 422  # Validation error

    def test_get_cliente_by_id_not_found(self, client, mock_cliente_service):
        mock_cliente_service.get_cliente_by_id.return_value = None

        with client.app.container.cliente_service.override(mock_cliente_service):
            response = client.get("/clientes/999")

        assert response.status_code == 404
