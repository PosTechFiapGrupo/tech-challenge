import pytest
from unittest.mock import AsyncMock, MagicMock
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.infrastructure.models.inventory_item_model import InventoryItemModel
from app.domain.entities.inventory_item_entity import InventoryItem


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.delete = AsyncMock()
    return db


@pytest.fixture
def repo(mock_db):
    return InventoryItemRepositoryImpl(mock_db)

@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_db):
    model = MagicMock(
        id=1,
        name="Item1",
        description="Desc1",
        quantity=10,
        minimum_stock=2,
        unit_price=100.0
    )
    model.name = "Item1"
    model.description = "Desc1"
    model.quantity = 10
    model.minimum_stock = 2
    model.unit_price = 100.0

    mock_db.get.return_value = model

    result = await repo.get_by_id(1)

    mock_db.get.assert_awaited_once_with(InventoryItemModel, 1)
    assert result.id == 1
    assert result.name == "Item1"


@pytest.mark.asyncio
async def test_create(repo, mock_db):
    item = InventoryItem(
        id=None,
        name="NewItem",
        description="NewDesc",
        quantity=5,
        minimum_stock=2,
        unit_price=50.0
    )

    db_item = MagicMock()
    db_item.id = 10
    db_item.name = item.name
    db_item.description = item.description
    db_item.quantity = item.quantity
    db_item.minimum_stock = item.minimum_stock
    db_item.unit_price = item.unit_price

    def add_side_effect(obj):
        obj.id = 10

    mock_db.add.side_effect = add_side_effect
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    original_to_entity = repo._to_entity
    repo._to_entity = lambda m: InventoryItem(
        id=m.id,
        name=m.name,
        description=m.description,
        quantity=m.quantity,
        minimum_stock=m.minimum_stock,
        unit_price=m.unit_price
    )

    result = await repo.create(item)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()
    assert result.id == 10
    assert result.name == "NewItem"

    repo._to_entity = original_to_entity


@pytest.mark.asyncio
async def test_update(repo, mock_db):
    db_item = MagicMock()
    db_item.id = 1
    db_item.name = "OldName"
    db_item.description = "OldDesc"
    db_item.quantity = 1
    db_item.minimum_stock = 1
    db_item.unit_price = 10.0

    mock_db.get.return_value = db_item
    mock_db.commit.return_value = None

    item = InventoryItem(
        id=1,
        name="UpdatedName",
        description="UpdatedDesc",
        quantity=5,
        minimum_stock=2,
        unit_price=50.0
    )

    original_to_entity = repo._to_entity
    repo._to_entity = lambda m: InventoryItem(
        id=m.id,
        name=m.name,
        description=m.description,
        quantity=m.quantity,
        minimum_stock=m.minimum_stock,
        unit_price=m.unit_price
    )

    result = await repo.update(1, item)

    mock_db.get.assert_awaited_once_with(InventoryItemModel, 1)
    mock_db.commit.assert_awaited_once()
    assert result.name == "UpdatedName"
    assert result.quantity == 5

    repo._to_entity = original_to_entity


@pytest.mark.asyncio
async def test_delete(repo, mock_db):
    db_item = MagicMock()
    mock_db.get.return_value = db_item
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    await repo.delete(1)

    mock_db.get.assert_awaited_once_with(InventoryItemModel, 1)
    mock_db.delete.assert_awaited_once_with(db_item)
    mock_db.commit.assert_awaited_once()
