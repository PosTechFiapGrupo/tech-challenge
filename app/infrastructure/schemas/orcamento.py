from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput
from app.infrastructure.schemas.servico import ServicoOutput
from app.infrastructure.schemas.inventory_item_schema import InventoryItemOut


class ServicoOrcamento(BaseModel):
    servico: ServicoOutput
    valor_na_os: Decimal
    observacoes: Optional[str] = None


class InventoryItemOrcamento(BaseModel):
    item: InventoryItemOut
    quantidade: int
    valor_unitario_na_os: Decimal
    valor_total: Decimal


class OrcamentoOutput(BaseModel):
    ordem_servico: OrdemServicoOutput
    servicos: List[ServicoOrcamento] = []
    inventory_items: List[InventoryItemOrcamento] = []
    total_servicos: Decimal
    total_items: Decimal
    total_geral: Decimal

    class Config:
        from_attributes = True
