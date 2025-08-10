import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.infrastructure.handlers.vehicle_handler import router
from app.infrastructure.container import Container
from app.domain.entities.vehicle import Vehicle


@pytest.fixture
def client():
    from fastapi import FastAPI
    app = FastAPI()
    container = Container()
    app.container = container
    app.include_router(router)
    container.wire(modules=["app.infrastructure.handlers.vehicle_handler"])
    return TestClient(app)


@pytest.fixture
def vehicle_data():
    return {
        "license_plate": "ABC1D23",
        "model": "TestModel",
        "brand": "TestBrand",
        "year": 2020
    }


@patch("app.infrastructure.handlers.vehicle_handler.validate_vehicle_plate", return_value=True)
@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_create_vehicle_success(mock_service_class, mock_validate_plate, client, vehicle_data):
    mock_service = AsyncMock()
    mock_service.criar_vehicle.return_value = Vehicle(id=1, **vehicle_data)
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.post("/vehicles/", json=vehicle_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["license_plate"] == vehicle_data["license_plate"]


@patch("app.infrastructure.handlers.vehicle_handler.validate_vehicle_plate", return_value=False)
def test_create_vehicle_invalid_plate(mock_validate_plate, client, vehicle_data):
    response = client.post("/vehicles/", json=vehicle_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "placa" in response.json()["detail"].lower()


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_create_vehicle_duplicate(mock_service_class, client, vehicle_data):
    from app.domain.exceptions import EntityAlreadyExists
    mock_service = AsyncMock()
    mock_service.criar_vehicle.side_effect = EntityAlreadyExists("já cadastrada")
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.post("/vehicles/", json=vehicle_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "já cadastrada" in response.json()["detail"].lower()


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_get_vehicle_success(mock_service_class, client, vehicle_data):
    mock_service = AsyncMock()
    mock_service.buscar_vehicle_por_id.return_value = Vehicle(id=1, **vehicle_data)
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.get("/vehicles/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["license_plate"] == vehicle_data["license_plate"]


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_get_vehicle_not_found(mock_service_class, client):
    from app.domain.exceptions import EntityNotFound
    mock_service = AsyncMock()
    mock_service.buscar_vehicle_por_id.side_effect = EntityNotFound("veículo não encontrado")
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.get("/vehicles/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "veículo não encontrado" in response.json()["detail"].lower()


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_list_vehicles(mock_service_class, client, vehicle_data):
    mock_service = AsyncMock()
    mock_service.listar_vehicles.return_value = [Vehicle(id=1, **vehicle_data)]
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.get("/vehicles/")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_update_vehicle_success(mock_service_class, client, vehicle_data):
    mock_service = AsyncMock()
    mock_service.atualizar_vehicle.return_value = Vehicle(id=1, **vehicle_data)
    mock_service_class.return_value = mock_service

    vehicle_data_with_id = {"id": 1, **vehicle_data}
    with client.app.container.vehicle_service.override(mock_service):
        response = client.put("/vehicles/", json=vehicle_data_with_id)

    assert response.status_code == status.HTTP_200_OK


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_update_vehicle_not_found(mock_service_class, client, vehicle_data):
    mock_service = AsyncMock()
    mock_service.atualizar_vehicle.return_value = None
    mock_service_class.return_value = mock_service

    vehicle_data_with_id = {"id": 1, **vehicle_data}
    with client.app.container.vehicle_service.override(mock_service):
        response = client.put("/vehicles/", json=vehicle_data_with_id)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "vehicle not found" in response.json()["detail"].lower()


@patch("app.infrastructure.handlers.vehicle_handler.VehicleService")
def test_delete_vehicle(mock_service_class, client):
    mock_service = AsyncMock()
    mock_service.deletar_vehicle.return_value = None
    mock_service_class.return_value = mock_service

    with client.app.container.vehicle_service.override(mock_service):
        response = client.delete("/vehicles/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT