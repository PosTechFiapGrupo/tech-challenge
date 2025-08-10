from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from app.infrastructure.database import Base


class OrdemServicoInventoryItemModel(Base):
    __tablename__ = "ordem_servico_inventory_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id = Column(String(36), ForeignKey("ordens_servico.id"), nullable=False)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(DECIMAL(precision=10, scale=2), nullable=False)
