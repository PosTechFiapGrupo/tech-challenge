import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.auth_dependencies import get_current_user
from app.infrastructure.schemas.inventory_item_schema import InventoryItemOut

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
def mock_inventory_item_service():
    mock = AsyncMock()
    mock.list_items = AsyncMock()
    mock.get_item = AsyncMock()
    mock.create_item = AsyncMock()
    mock.update_item = AsyncMock()
    mock.delete_item = AsyncMock()
    return mock

@pytest.fixture(scope="function")
def override_services(app, mock_inventory_item_service, mock_user_service):
    app.container.inventory_item_use_case.override(mock_inventory_item_service)
    app.container.user_service.override(mock_user_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.inventory_item_use_case.reset_override()
    app.container.user_service.reset_override()
    app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestInventoryItemAPI:

    async def test_list_items_empty(self, async_client, override_services, mock_inventory_item_service):
        mock_inventory_item_service.list_items.return_value = []

        response = await async_client.get("/inventory/")

        assert response.status_code == 200
        assert response.json() == []

    async def test_get_item_success(self, async_client, override_services, mock_inventory_item_service):
        mock_item = InventoryItemOut(
            id=1,
            name="Item 1",
            description="Descrição do item 1",
            quantity=10,
            minimum_stock=2,
            unit_price=15.5
        )
        mock_inventory_item_service.get_item.return_value = mock_item

        response = await async_client.get("/inventory/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Item 1"

    async def test_get_item_not_found(self, async_client, override_services, mock_inventory_item_service):
        async def raise_404(item_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        mock_inventory_item_service.get_item.side_effect = raise_404

        response = await async_client.get("/inventory/999")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Item not found"

    async def test_create_item_success(self, async_client, override_services, mock_inventory_item_service):
        item_data = {
            "name": "Novo Item",
            "description": "Descrição do novo item",
            "quantity": 5,
            "minimum_stock": 1,
            "unit_price": 20.0,
        }

        mock_item = InventoryItemOut(id=1, **item_data)
        mock_inventory_item_service.create_item.return_value = mock_item

        response = await async_client.post("/inventory/", json=item_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Novo Item"
        assert data["unit_price"] == 20.0

    async def test_update_item_success(self, async_client, override_services, mock_inventory_item_service):
        item_data = {
            "name": "Item Atualizado",
            "description": "Descrição atualizada",
            "quantity": 7,
            "minimum_stock": 2,
            "unit_price": 25.0,
        }

        mock_item = InventoryItemOut(id=1, **item_data)
        mock_inventory_item_service.update_item.return_value = mock_item

        response = await async_client.put("/inventory/1", json=item_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Item Atualizado"
        assert data["unit_price"] == 25.0

    async def test_delete_item_success(self, async_client, override_services, mock_inventory_item_service):
        mock_inventory_item_service.delete_item.return_value = None

        response = await async_client.delete("/inventory/1")

        assert response.status_code == 204
