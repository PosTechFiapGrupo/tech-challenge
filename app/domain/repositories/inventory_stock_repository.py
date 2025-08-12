from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from app.domain.entities.inventory_movement_entity import InventoryMovement

class InventoryStockRepository(ABC):
    @abstractmethod
    async def add_entry(self, item_id: int, quantity: int, note: Optional[str]): ...
    @abstractmethod
    async def consume_for_os(self, os_id: str, items: List[Dict[str, int]]): ...
    @abstractmethod
    async def list_movements(self, item_id: int, limit: int = 50) -> List[InventoryMovement]: ...
