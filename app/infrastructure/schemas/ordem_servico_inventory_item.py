from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class AddInventoryItemToOrdemServicoInput(BaseModel):
    """Schema para adicionar um item de inventário a uma ordem de serviço"""
    inventory_item_id: int
    quantidade: int


class OrdemServicoInventoryItemOutput(BaseModel):
    """Schema de saída para relação ordem_servico-inventory_item"""
    ordem_servico_id: str
    inventory_item_id: int
    quantidade: int
    valor_unitario: Decimal

    class Config:
        from_attributes = True
