from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.servico import ServicoEntity


class ServicoRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[ServicoEntity]:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, id: str) -> ServicoEntity:
        raise NotImplemented

    @abstractmethod
    async def add(self, servico: ServicoEntity) -> ServicoEntity:
        raise NotImplemented

    @abstractmethod
    async def update(self, servico: ServicoEntity) -> ServicoEntity:
        raise NotImplemented

    @abstractmethod
    async def delete(self, id: str) -> bool:
        raise NotImplemented
