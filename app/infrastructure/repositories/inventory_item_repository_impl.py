from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.entities.inventory_item_entity import InventoryItem
from app.domain.repositories.inventory_item_repository import InventoryItemRepository
from app.infrastructure.models.inventory_item_model import InventoryItemModel

class InventoryItemRepositoryImpl(InventoryItemRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self):
        result = await self.db.execute(select(InventoryItemModel))
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get_by_id(self, item_id: int):
        result = await self.db.get(InventoryItemModel, item_id)
        return self._to_entity(result)

    async def create(self, item: InventoryItem):
        db_item = InventoryItemModel(
            name=item.name,
            description=item.description,
            quantity=item.quantity,
            minimum_stock=item.minimum_stock,
            unit_price=item.unit_price,
        )
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return self._to_entity(db_item)

    async def update(self, item_id: int, item: InventoryItem):
        db_item = await self.db.get(InventoryItemModel, item_id)
        db_item.name = item.name
        db_item.description = item.description
        db_item.quantity = item.quantity
        db_item.minimum_stock = item.minimum_stock
        db_item.unit_price = item.unit_price
        await self.db.commit()
        return self._to_entity(db_item)


    async def delete(self, item_id: int):
        db_item = await self.db.get(InventoryItemModel, item_id)
        await self.db.delete(db_item)
        await self.db.commit()

    def _to_entity(self, model: InventoryItemModel) -> InventoryItem:
        return InventoryItem(
            id=model.id,
            name=model.name,
            description=model.description,
            quantity=model.quantity,
            minimum_stock=model.minimum_stock,
            unit_price=model.unit_price,
        )