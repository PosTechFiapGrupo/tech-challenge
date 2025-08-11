from decimal import Decimal
from typing import Optional


class OrdemServicoInventoryItemEntity:
    def __init__(
        self,
        id: Optional[int],
        ordem_servico_id: str,
        inventory_item_id: int,
        quantidade: int,
        valor_unitario: Decimal,
    ):
        self.id = id
        self.ordem_servico_id = ordem_servico_id
        self.inventory_item_id = inventory_item_id
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    @property
    def valor_total(self) -> Decimal:
        return self.quantidade * self.valor_unitario


class OrdemServicoInventoryItemEntityFactory:
    @staticmethod
    def create(
        id: Optional[int],
        ordem_servico_id: str,
        inventory_item_id: int,
        quantidade: int,
        valor_unitario: Decimal,
    ) -> OrdemServicoInventoryItemEntity:
        return OrdemServicoInventoryItemEntity(
            id=id,
            ordem_servico_id=ordem_servico_id,
            inventory_item_id=inventory_item_id,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
        )
