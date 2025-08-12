import pytest
from unittest.mock import AsyncMock, MagicMock, ANY
from app.infrastructure.repositories.inventory_stock_repository_impl import InventoryStockRepositoryImpl
from app.infrastructure.models.inventory_movement_model import MovementType

@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    return db

@pytest.fixture
def repo(mock_db):
    return InventoryStockRepositoryImpl(mock_db)

@pytest.mark.asyncio
async def test_consume_for_os_success(repo, mock_db):
    
    mock_row = MagicMock()
    mock_row.id = 1
    mock_row.quantity = 10

    
    mock_result = MagicMock()
    mock_result.first = AsyncMock(return_value=mock_row)

    
    async def execute_side_effect(*args, **kwargs):
        if "SELECT" in args[0].text:
            return mock_result
        else:
            return AsyncMock()

    mock_db.execute.side_effect = execute_side_effect

    items = [
        {"item_id": 1, "quantity": 2},
        {"item_id": 2, "quantity": 5},
    ]

    await repo.consume_for_os("os123", items)

    update_calls = [call for call in mock_db.execute.call_args_list if call[0][0].text.startswith("UPDATE")]
    assert len(update_calls) == 2

    adds = mock_db.add.call_args_list
    assert len(adds) == 2
    for call, item in zip(adds, items):
        movement = call[0][0]
        assert movement.item_id == item["item_id"]
        assert movement.type == MovementType.SAIDA
        assert movement.quantity == item["quantity"]
        assert movement.os_id == "os123"
        assert movement.note == "Baixa por OS"

    mock_db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_consume_for_os_item_not_found(repo, mock_db):
    mock_result = MagicMock()
    mock_result.first = AsyncMock(return_value=None)  # nenhum registro encontrado

    async def execute_side_effect(*args, **kwargs):
        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    items = [{"item_id": 99, "quantity": 1}]

    with pytest.raises(ValueError, match="Item 99 não encontrado"):
        await repo.consume_for_os("os123", items)

@pytest.mark.asyncio
async def test_consume_for_os_insufficient_stock(repo, mock_db):
    mock_row = MagicMock()
    mock_row.id = 1
    mock_row.quantity = 1  # estoque menor que quantidade solicitada

    mock_result = MagicMock()
    mock_result.first = AsyncMock(return_value=mock_row)

    async def execute_side_effect(*args, **kwargs):
        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    items = [{"item_id": 1, "quantity": 5}]

    with pytest.raises(ValueError, match="Estoque insuficiente para item 1"):
        await repo.consume_for_os("os123", items)
