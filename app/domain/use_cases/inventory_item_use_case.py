from app.domain.entities.inventory_item_entity import InventoryItem
from app.domain.repositories.inventory_item_repository import InventoryItemRepository
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class InventoryItemUseCase:
    def __init__(self, repository: InventoryItemRepository):
        self.repository = repository

    async def list_items(self):
        items = await self.repository.list_all()
        logger.info("Itens de inventário listados", extra={"count": len(items)})
        return items

    async def get_item(self, item_id: int):
        item = await self.repository.get_by_id(item_id)
        logger.info("Item de inventário buscado", extra={"item_id": item_id})
        return item

    async def create_item(self, item: InventoryItem):
        created = await self.repository.create(item)
        logger.info("Item de inventário criado", extra={"item_id": created.id, "name": item.name})
        return created

    async def update_item(self, item_id: int, item: InventoryItem):
        updated = await self.repository.update(item_id, item)
        logger.info("Item de inventário atualizado", extra={"item_id": item_id})
        return updated

    async def delete_item(self, item_id: int):
        await self.repository.delete(item_id)
        logger.info("Item de inventário deletado", extra={"item_id": item_id})
