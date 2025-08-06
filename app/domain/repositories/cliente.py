from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.cliente import ClienteEntity


class ClienteRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[ClienteEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def add(self, cliente: ClienteEntity) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, cliente: ClienteEntity) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> bool:
        raise NotImplementedError
