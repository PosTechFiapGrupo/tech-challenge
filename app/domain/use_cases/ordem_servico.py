from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.ordem_servico import OrdemServicoEntity


class OrdemServicoUseCases(ABC):

    @abstractmethod
    async def create_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_ordem_servico_by_id(self, id: str) -> OrdemServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all_ordens_servico(self) -> List[OrdemServicoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        raise NotImplementedError
