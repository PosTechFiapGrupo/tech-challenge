import pytest
from datetime import datetime
from app.domain.entities.inventory_movement_entity import InventoryMovement

class TestInventoryMovement:

    def test_create_inventory_movement_with_all_fields(self):
        now = datetime.utcnow()
        movimento = InventoryMovement(
            id=1,
            item_id=10,
            type="entrada",
            quantity=5,
            os_id="os-123",
            note="Reabastecimento",
            created_at=now
        )
        assert movimento.id == 1
        assert movimento.item_id == 10
        assert movimento.type == "entrada"
        assert movimento.quantity == 5
        assert movimento.os_id == "os-123"
        assert movimento.note == "Reabastecimento"
        assert movimento.created_at == now

    def test_create_inventory_movement_with_optional_none(self):
        now = datetime.utcnow()
        movimento = InventoryMovement(
            id=2,
            item_id=20,
            type="consumo",
            quantity=3,
            os_id=None,
            note=None,
            created_at=now
        )
        assert movimento.os_id is None
        assert movimento.note is None
