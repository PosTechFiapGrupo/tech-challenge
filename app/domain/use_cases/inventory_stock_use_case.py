from typing import Dict, List, Optional

from app.domain.repositories.inventory_stock_repository import InventoryStockRepository
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class InventoryStockUseCase:
    def __init__(self, repo: InventoryStockRepository):
        self.repo = repo

    async def entrada(self, item_id: int, quantity: int, note: Optional[str]):
        await self.repo.add_entry(item_id, quantity, note)
        logger.info("Entrada de estoque registrada", extra={"item_id": item_id, "quantity": quantity})

    async def consumir_para_os(self, os_id: str, items: List[Dict[str, int]]):
        await self.repo.consume_for_os(os_id, items)
        logger.info("Estoque consumido para OS", extra={"os_id": os_id, "items_count": len(items)})

    async def listar_movimentos(self, item_id: int, limit: int = 50):
        movimentos = await self.repo.list_movements(item_id, limit)
        logger.info("Movimentos de estoque listados", extra={"item_id": item_id, "count": len(movimentos)})
        return movimentos
