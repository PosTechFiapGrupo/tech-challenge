from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.inventory_item import InventoryItem
from app.infrastructure.models.inventory_item_model import InventoryItemModel

class InventoryItemRepositoryImpl:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> Optional[InventoryItem]:
        query = await self.db.execute(
            select(InventoryItemModel).filter_by(id=item_id)
        )
        model = query.scalar_one_or_none()
        return model.to_entity() if model else None

    async def list_all(self) -> List[InventoryItem]:
        query = await self.db.execute(select(InventoryItemModel))
        inventory_models = query.scalars().all()
        return [inventory.to_entity() for inventory in inventory_models]

    async def create(self, entity: InventoryItem) -> InventoryItem:
        model = InventoryItemModel(
            name=entity.name,
            description=entity.description,
            quantity=entity.quantity,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model.to_entity()

    async def update(self, entity: InventoryItem) -> Optional[InventoryItem]:
        model = await self.db.get(InventoryItemModel, entity.id)
        if not model:
            return None

        model.name = entity.name
        model.description = entity.description
        model.quantity = entity.quantity

        await self.db.commit()
        await self.db.refresh(model)
        return model.to_entity()

    async def delete(self, item_id: int) -> None:
        model = await self.db.get(InventoryItemModel, item_id)
        if model:
            await self.db.delete(model)
            await self.db.commit()
