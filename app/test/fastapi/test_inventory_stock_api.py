import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.auth_dependencies import get_current_user
from app.infrastructure.schemas.inventory_stock_schema import EntryRequest, ConsumeRequest, MovementOut

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

    mock.get_user_by_email.side_effect = get_user_by_email
    return mock

@pytest.fixture(scope="function")
def mock_inventory_stock_service():
    mock = AsyncMock()
    mock.entrada = AsyncMock()
    mock.consumir_para_os = AsyncMock()
    mock.listar_movimentos = AsyncMock()
    return mock

@pytest.fixture(scope="function")
def override_services(app, mock_inventory_stock_service, mock_user_service):
    app.container.inventory_stock_use_case.override(mock_inventory_stock_service)
    app.container.user_service.override(mock_user_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.inventory_stock_use_case.reset_override()
    app.container.user_service.reset_override()
    app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestInventoryStockAPI:

    async def test_add_entry_success(self, async_client, override_services, mock_inventory_stock_service):
        payload = {"quantity": 10, "note": "Entrada de teste"}
        mock_inventory_stock_service.entrada.return_value = None

        response = await async_client.post("/inventory/1/entries", json=payload)

        assert response.status_code == 204
        mock_inventory_stock_service.entrada.assert_awaited_once_with(1, 10, "Entrada de teste")

    async def test_consume_stock_success(self, async_client, override_services, mock_inventory_stock_service):
        payload = {
            "os_id": "os123",
            "items": [
                {"item_id": 1, "quantity": 2},
                {"item_id": 2, "quantity": 3}
            ]
        }
        mock_inventory_stock_service.consumir_para_os.return_value = None

        response = await async_client.post("/inventory/consume", json=payload)

        assert response.status_code == 204
        mock_inventory_stock_service.consumir_para_os.assert_awaited_once()
        called_args = mock_inventory_stock_service.consumir_para_os.call_args[0]
        assert called_args[0] == "os123"
        assert isinstance(called_args[1], list)
        assert called_args[1][0]["item_id"] == 1

    async def test_consume_stock_conflict(self, async_client, override_services, mock_inventory_stock_service):
        payload = {
            "os_id": "os123",
            "items": [{"item_id": 1, "quantity": 1000}]
        }

        async def raise_conflict(os_id, items):
            raise ValueError("Quantidade insuficiente no estoque")

        mock_inventory_stock_service.consumir_para_os.side_effect = raise_conflict

        response = await async_client.post("/inventory/consume", json=payload)

        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "Quantidade insuficiente" in data["detail"]

    async def test_list_movements_success(self, async_client, override_services, mock_inventory_stock_service):
        mock_movement = MovementOut(
            id=1,
            item_id=1,
            quantity=5,
            note="Movimento teste",
            type="entry",
            created_at="2025-08-12T19:00:00"
        )
        mock_inventory_stock_service.listar_movimentos.return_value = [mock_movement]

        response = await async_client.get("/inventory/1/movements")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["id"] == 1
        assert data[0]["type"] == "entry"
