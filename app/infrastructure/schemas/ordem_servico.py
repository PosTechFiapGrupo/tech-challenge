from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoStatusQuery(BaseModel):
    status: StatusOrdemServico

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if not isinstance(v, StatusOrdemServico):
            # Tentar converter string para enum
            if isinstance(v, str):
                try:
                    return StatusOrdemServico(v)
                except ValueError:
                    valid_values = ", ".join([status.value for status in StatusOrdemServico])
                    raise ValueError(f"Status inválido. Valores válidos: {valid_values}")
        return v


class OrdemServicoInput(BaseModel):
    cliente_id: str
    vehicle_id: int
    servico_ids: List[str]
    atendente_id: Optional[str] = None
    mecanico_id: Optional[str] = None
    orcamento_id: Optional[str] = None
    status: Optional[StatusOrdemServico] = StatusOrdemServico.RECEBIDA


class OrdemServicoUpdate(BaseModel):
    status: Optional[StatusOrdemServico] = None
    mecanico_id: Optional[str] = None
    orcamento_id: Optional[str] = None
    data_fechamento: Optional[datetime] = None


class OrdemServicoOutput(BaseModel):
    id: str
    cliente_id: str
    vehicle_id: int
    servico_ids: List[str]
    status: StatusOrdemServico
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    atendente_id: Optional[str] = None
    mecanico_id: Optional[str] = None
    orcamento_id: Optional[str] = None

    class Config:
        from_attributes = True
