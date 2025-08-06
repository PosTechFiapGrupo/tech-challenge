from app.domain.repositories.inventory_item_repository import InventoryItemRepository
from app.domain.entities.inventory_item_entity import InventoryItem

class InventoryItemUseCase:
    def __init__(self, repository: InventoryItemRepository):
        self.repository = repository

    async def list_items(self):
        return await self.repository.list_all()

    async def get_item(self, item_id: int):
        return await self.repository.get_by_id(item_id)

    async def create_item(self, item: InventoryItem):
        return await self.repository.create(item)

    async def update_item(self, item_id: int, item: InventoryItem):
        return await self.repository.update(item_id, item)

    async def delete_item(self, item_id: int):
        await self.repository.delete(item_id)
