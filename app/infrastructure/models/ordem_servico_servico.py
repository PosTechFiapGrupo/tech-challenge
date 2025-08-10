from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from app.infrastructure.database import Base


class OrdemServicoServicoModel(Base):
    __tablename__ = "ordem_servico_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id = Column(String(36), ForeignKey("ordens_servico.id"), nullable=False)
    servico_id = Column(String(36), ForeignKey("servicos.id"), nullable=False)
    valor_servico = Column(DECIMAL(precision=10, scale=2), nullable=False)
    observacoes = Column(String(500), nullable=True)
