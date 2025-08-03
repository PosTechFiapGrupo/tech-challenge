from typing import List, Optional
from app.domain.entities.inventory_item import InventoryItem
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl

class InventoryItemUseCase:
    def __init__(self, repository: InventoryItemRepositoryImpl):
        self.repository = repository

    async def get(self, item_id: int) -> Optional[InventoryItem]:
        return await self.repository.get_by_id(item_id)

    async def list_all(self) -> List[InventoryItem]:
        return await self.repository.list_all()

    async def create(self, item: InventoryItem):
        return await self.repository.create(item)

    async def update(self, item: InventoryItem) -> Optional[InventoryItem]:
        return await self.repository.update(item)

    async def delete(self, item_id: int) -> None:
        await self.repository.delete(item_id)
