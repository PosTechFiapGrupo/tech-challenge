from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoRepository(ABC):

    @abstractmethod
    async def create(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> OrdemServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[OrdemServicoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_status(self, status: StatusOrdemServico) -> List[OrdemServicoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        raise NotImplementedError
