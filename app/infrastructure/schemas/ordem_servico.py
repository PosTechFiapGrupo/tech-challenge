from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoInput(BaseModel):
    cliente_id: str
    veiculo_id: str
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
    veiculo_id: str
    servico_ids: List[str]
    status: StatusOrdemServico
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    atendente_id: Optional[str] = None
    mecanico_id: Optional[str] = None
    orcamento_id: Optional[str] = None

    class Config:
        from_attributes = True
