from sqlalchemy import Column, Integer, String, DECIMAL
from app.infrastructure.database import Base

class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    quantity = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    unit_price = Column(DECIMAL(precision=10, scale=2), nullable=False)
