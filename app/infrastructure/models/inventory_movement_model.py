from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from datetime import datetime
import enum
from app.infrastructure.database import Base

class MovementType(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    AJUSTE = "AJUSTE"

class InventoryMovementModel(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False, index=True)
    os_id = Column(String(36), index=True, nullable=True)
    type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    note = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
