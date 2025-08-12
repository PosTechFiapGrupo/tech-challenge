from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.status_ordem_servico import StatusOrdemServico


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
    async def get_ordens_servico_by_status(self, status: StatusOrdemServico) -> List[OrdemServicoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        raise NotImplementedError
