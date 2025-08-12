from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.infrastructure.models.inventory_item_model import InventoryItemModel
from app.infrastructure.models.inventory_movement_model import InventoryMovementModel, MovementType
from app.domain.entities.inventory_movement_entity import InventoryMovement
from app.domain.repositories.inventory_stock_repository import InventoryStockRepository

class InventoryStockRepositoryImpl(InventoryStockRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_entry(self, item_id: int, quantity: int, note: Optional[str]):
        await self.db.execute(
            text("UPDATE inventory_items SET quantity = quantity + :q WHERE id=:id"),
            {"q": quantity, "id": item_id}
        )
        self.db.add(InventoryMovementModel(
            item_id=item_id, type=MovementType.ENTRADA, quantity=quantity, note=note
        ))
        await self.db.commit()

    async def consume_for_os(self, os_id: str, items: List[Dict[str, int]]):
        # trava e valida
        for it in items:
            result = await self.db.execute(
                text("SELECT id, quantity FROM inventory_items WHERE id=:id FOR UPDATE"),
                {"id": it["item_id"]}
            )
            row = await result.first()  # <--- await aqui
            if not row:
                raise ValueError(f"Item {it['item_id']} não encontrado")
            if row.quantity < it["quantity"]:
                raise ValueError(f"Estoque insuficiente para item {it['item_id']}")

        # baixa
        for it in items:
            await self.db.execute(
                text("UPDATE inventory_items SET quantity = quantity - :q WHERE id=:id"),
                {"q": it["quantity"], "id": it["item_id"]}
            )
            self.db.add(InventoryMovementModel(
                item_id=it["item_id"], os_id=os_id, type=MovementType.SAIDA,
                quantity=it["quantity"], note="Baixa por OS"
            ))
        await self.db.commit()

    async def list_movements(self, item_id: int, limit: int = 50):
        res = await self.db.execute(
            select(InventoryMovementModel)
            .where(InventoryMovementModel.item_id == item_id)
            .order_by(InventoryMovementModel.id.desc())
            .limit(limit)
        )
        rows = res.scalars().all()
        return [InventoryMovement(
            id=r.id, item_id=r.item_id, type=r.type.value, quantity=r.quantity,
            os_id=r.os_id, note=r.note, created_at=r.created_at
        ) for r in rows]
