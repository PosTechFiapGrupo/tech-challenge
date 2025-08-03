from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base 
from app.domain.entities.inventory_item import InventoryItem

class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    quantity = Column(Integer, nullable=False)

    def to_entity(self) -> InventoryItem:
        return InventoryItem(
            id=self.id,
            name=self.name,
            description=self.description,
            quantity=self.quantity,
        )
