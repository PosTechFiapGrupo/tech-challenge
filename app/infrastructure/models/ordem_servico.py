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

# Tabela associativa entre Ordem de Serviço e Serviços
ordem_servico_servico = Table(
    "ordem_servico_servico",
    Base.metadata,
    Column(
        "ordem_servico_id", Integer, ForeignKey("ordens_servico.id"), primary_key=True
    ),
    Column("servico_id", Integer, ForeignKey("servicos.id"), primary_key=True),
)


class OrdemServicoModel(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    veiculo_id = Column(Integer, nullable=False)  # futuro ForeignKey("veiculos.id")
    mecanico_id = Column(Integer, nullable=True)
    atendente_id = Column(Integer, nullable=True)
    orcamento_id = Column(Integer, nullable=True)
    status = Column(String(30), nullable=False, default="recebida")
    data_abertura = Column(DateTime, nullable=False, server_default=func.now())
    data_fechamento = Column(DateTime, nullable=True)

    # Relacionamento com serviços
    servicos = relationship(
        "ServicoModel",
        secondary=ordem_servico_servico,
        backref="ordens_servico",
        lazy="joined",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "veiculo_id": self.veiculo_id,
            "mecanico_id": self.mecanico_id,
            "atendente_id": self.atendente_id,
            "orcamento_id": self.orcamento_id,
            "status": self.status,
            "data_abertura": (
                self.data_abertura.isoformat() if self.data_abertura else None
            ),
            "data_fechamento": (
                self.data_fechamento.isoformat() if self.data_fechamento else None
            ),
            "servico_ids": [s.id for s in self.servicos],
        }
