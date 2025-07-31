import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_servico_service():
    return AsyncMock()


class TestServicoAPI:

    def test_get_all_servicos_empty(self, client, mock_servico_service):
        # Mock the service to return empty list
        mock_servico_service.get_all_servicos.return_value = []

        with client.app.container.servico_service.override(mock_servico_service):
            response = client.get("/servicos/")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_servico_success(self, client, mock_servico_service):
        servico_data = {"descricao": "Consultoria em TI", "preco": 150.00}

        from app.domain.entities.servico import ServicoEntity

        mock_servico = ServicoEntity("1", "Consultoria em TI", 150.00)
        mock_servico_service.create_servico.return_value = mock_servico

        with client.app.container.servico_service.override(mock_servico_service):
            response = client.post("/servicos/", json=servico_data)

        assert response.status_code == 201
        data = response.json()
        assert data["descricao"] == "Consultoria em TI"
        assert data["preco"] == 150.00

    def test_create_servico_invalid_price(self, client):
        servico_data = {"descricao": "Consultoria em TI", "preco": -50.00}

        response = client.post("/servicos/", json=servico_data)
        assert response.status_code == 422  # Validation error

    def test_get_servico_by_id_not_found(self, client, mock_servico_service):
        mock_servico_service.get_servico_by_id.return_value = None

        with client.app.container.servico_service.override(mock_servico_service):
            response = client.get("/servicos/999")

        assert response.status_code == 404
