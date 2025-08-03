from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.inventory_item_entity import InventoryItem

class InventoryItemRepository(ABC):
    @abstractmethod
    async def list_all(self) -> List[InventoryItem]: ...
    
    @abstractmethod
    async def get_by_id(self, item_id: int) -> InventoryItem: ...
    
    @abstractmethod
    async def create(self, item: InventoryItem) -> InventoryItem: ...
    
    @abstractmethod
    async def update(self, item_id: int, item: InventoryItem) -> InventoryItem: ...
    
    @abstractmethod
    async def delete(self, item_id: int) -> None: ...
