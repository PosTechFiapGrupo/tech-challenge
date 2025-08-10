from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.ordem_servico_servico import OrdemServicoServicoEntity


class OrdemServicoServicoRepository(ABC):
    
    @abstractmethod
    async def adicionar_servico_a_os(
        self, os_servico: OrdemServicoServicoEntity
    ) -> OrdemServicoServicoEntity:
        pass
    
    @abstractmethod
    async def listar_servicos_por_os(self, ordem_servico_id: str) -> List[OrdemServicoServicoEntity]:
        pass
    
    @abstractmethod
    async def remover_servico_da_os(self, ordem_servico_id: str, servico_id: str) -> bool:
        pass
