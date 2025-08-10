from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.ordem_servico_inventory_item import OrdemServicoInventoryItemEntity


class OrdemServicoInventoryItemRepository(ABC):
    
    @abstractmethod
    async def adicionar_item_a_os(
        self, os_item: OrdemServicoInventoryItemEntity
    ) -> OrdemServicoInventoryItemEntity:
        pass
    
    @abstractmethod
    async def listar_itens_por_os(self, ordem_servico_id: str) -> List[OrdemServicoInventoryItemEntity]:
        pass
    
    @abstractmethod
    async def remover_item_da_os(self, ordem_servico_id: str, inventory_item_id: int) -> bool:
        pass
