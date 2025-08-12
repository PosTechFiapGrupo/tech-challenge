import pytest
from pydantic import ValidationError
from datetime import datetime
from app.infrastructure.schemas.inventory_stock_schema import (
    EntryRequest, ConsumeItem, ConsumeRequest, MovementOut
)

class TestInventoryStockSchemas:

    def test_entry_request_valid(self):
        entry = EntryRequest(quantity=5, note="Entrada de teste")
        assert entry.quantity == 5
        assert entry.note == "Entrada de teste"

    def test_entry_request_invalid_quantity(self):
        with pytest.raises(ValidationError):
            EntryRequest(quantity=0)  # quantity must be > 0

    def test_consume_item_valid(self):
        item = ConsumeItem(item_id=10, quantity=3)
        assert item.item_id == 10
        assert item.quantity == 3

    def test_consume_item_invalid_quantity(self):
        with pytest.raises(ValidationError):
            ConsumeItem(item_id=10, quantity=0)  # quantity must be > 0

    def test_consume_request_valid(self):
        items = [ConsumeItem(item_id=1, quantity=2), ConsumeItem(item_id=2, quantity=1)]
        consume = ConsumeRequest(os_id="os123", items=items)
        assert consume.os_id == "os123"
        assert len(consume.items) == 2

    def test_movement_out_from_attributes(self):
        class FakeORM:
            def __init__(self):
                self.id = 1
                self.item_id = 100
                self.os_id = "os123"
                self.type = "entrada"
                self.quantity = 10
                self.note = "Teste de movimento"
                self.created_at = datetime(2025, 8, 12, 15, 0)

        orm_obj = FakeORM()
        movement = MovementOut.from_orm(orm_obj)
        assert movement.id == 1
        assert movement.item_id == 100
        assert movement.os_id == "os123"
        assert movement.type == "entrada"
        assert movement.quantity == 10
        assert movement.note == "Teste de movimento"
        assert movement.created_at == datetime(2025, 8, 12, 15, 0)
