from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class AddServicoToOrdemServicoInput(BaseModel):
    """Schema para adicionar um serviço a uma ordem de serviço"""
    servico_id: str
    observacoes: Optional[str] = None


class OrdemServicoServicoOutput(BaseModel):
    """Schema de saída para relação ordem_servico-serviço"""
    ordem_servico_id: str
    servico_id: str
    valor_servico: Decimal
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True
