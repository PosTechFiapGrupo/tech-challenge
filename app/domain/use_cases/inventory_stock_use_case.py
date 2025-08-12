from typing import List, Dict, Optional
from app.domain.repositories.inventory_stock_repository import InventoryStockRepository

class InventoryStockUseCase:
    def __init__(self, repo: InventoryStockRepository):
        self.repo = repo

    async def entrada(self, item_id: int, quantity: int, note: Optional[str]):
        await self.repo.add_entry(item_id, quantity, note)

    async def consumir_para_os(self, os_id: str, items: List[Dict[str, int]]):
        await self.repo.consume_for_os(os_id, items)

    async def listar_movimentos(self, item_id: int, limit: int = 50):
        return await self.repo.list_movements(item_id, limit)
