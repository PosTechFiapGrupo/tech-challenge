import pytest
from app.domain.entities.inventory_item_entity import InventoryItem

class TestInventoryItem:

    def test_create_inventory_item_with_valid_data(self):
        item = InventoryItem(
            id=1,
            name="Óleo de motor",
            description="Óleo sintético 5W30",
            quantity=10,
            minimum_stock=2,
            unit_price=25.50
        )
        assert item.id == 1
        assert item.name == "Óleo de motor"
        assert item.description == "Óleo sintético 5W30"
        assert item.quantity == 10
        assert item.minimum_stock == 2
        assert item.unit_price == 25.50

    def test_create_inventory_item_without_id(self):
        item = InventoryItem(
            id=None,
            name="Filtro de óleo",
            description="Filtro para motor",
            quantity=5,
            minimum_stock=1,
            unit_price=15.75
        )
        assert item.id is None
        assert item.name == "Filtro de óleo"
