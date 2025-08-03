from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.inventory_item import InventoryItem

class InventoryItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[InventoryItem]:
        pass

    @abstractmethod
    def list_all(self) -> List[InventoryItem]:
        pass

    @abstractmethod
    def create(self, item: InventoryItem) -> InventoryItem:
        pass

    @abstractmethod
    def update(self, item: InventoryItem) -> InventoryItem:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        pass
