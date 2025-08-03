from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.database import Base

class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    unit_price = Column(Float, nullable=False)
