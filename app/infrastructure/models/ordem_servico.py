from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class OrdemServicoModel(Base):
    __tablename__ = "ordens_servico"

    id = Column(String(36), primary_key=True)
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    mecanico_id = Column(String(36), nullable=True)
    atendente_id = Column(String(36), nullable=True)
    orcamento_id = Column(String(36), nullable=True)
    status = Column(String(30), nullable=False, default="recebida")
    data_abertura = Column(DateTime, nullable=False, server_default=func.now())
    data_fechamento = Column(DateTime, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "vehicle_id": self.vehicle_id,
            "mecanico_id": self.mecanico_id,
            "atendente_id": self.atendente_id,
            "orcamento_id": self.orcamento_id,
            "status": self.status,
            "data_abertura": self.data_abertura,
            "data_fechamento": self.data_fechamento,
            "servico_ids": [],  # Este será preenchido pelos repositórios quando necessário
        }
