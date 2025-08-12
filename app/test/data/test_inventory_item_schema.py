import pytest
from pydantic import ValidationError
from app.infrastructure.schemas.inventory_item_schema import InventoryItemCreate, InventoryItemUpdate, InventoryItemOut

class TestInventoryItemSchemas:

    def test_inventory_item_create_valid(self):
        data = InventoryItemCreate(
            name="Óleo de motor",
            description="Lubrificante 5W30",
            quantity=10,
            minimum_stock=3,
            unit_price=89.90
        )
        assert data.name == "Óleo de motor"
        assert data.unit_price == 89.90

    def test_inventory_item_create_missing_fields(self):
        with pytest.raises(ValidationError):
            InventoryItemCreate(
                name="",
                description="",
                quantity=None,
                minimum_stock=None,
                unit_price=None
            )

    def test_inventory_item_update_valid(self):
        data = InventoryItemUpdate(
            name="Filtro de óleo",
            description="Filtro para motor",
            quantity=5,
            minimum_stock=1,
            unit_price=45.0
        )
        assert data.name == "Filtro de óleo"

    def test_inventory_item_out_from_attributes(self):
        # Criando uma instância simulando dados do ORM com atributos
        class FakeORM:
            def __init__(self):
                self.id = 1
                self.name = "Bateria"
                self.description = "Bateria 12V"
                self.quantity = 20
                self.minimum_stock = 5
                self.unit_price = 250.0

        orm_obj = FakeORM()
        schema_obj = InventoryItemOut.from_orm(orm_obj)
        assert schema_obj.id == 1
        assert schema_obj.name == "Bateria"
