import pytest
from decimal import Decimal
from app.domain.entities.ordem_servico_inventory_item import (
    OrdemServicoInventoryItemEntity,
    OrdemServicoInventoryItemEntityFactory,
)

class TestOrdemServicoInventoryItemEntity:

    def test_create_entity_properties(self):
        item = OrdemServicoInventoryItemEntity(
            id=1,
            ordem_servico_id="os-123",
            inventory_item_id=10,
            quantidade=3,
            valor_unitario=Decimal("15.50"),
        )
        assert item.id == 1
        assert item.ordem_servico_id == "os-123"
        assert item.inventory_item_id == 10
        assert item.quantidade == 3
        assert item.valor_unitario == Decimal("15.50")
        assert item.valor_total == Decimal("46.50")  # 3 * 15.50

    def test_factory_create_entity(self):
        item = OrdemServicoInventoryItemEntityFactory.create(
            id=None,
            ordem_servico_id="os-456",
            inventory_item_id=20,
            quantidade=5,
            valor_unitario=Decimal("10.00"),
        )
        assert item.id is None
        assert item.ordem_servico_id == "os-456"
        assert item.inventory_item_id == 20
        assert item.quantidade == 5
        assert item.valor_unitario == Decimal("10.00")
        assert item.valor_total == Decimal("50.00")
