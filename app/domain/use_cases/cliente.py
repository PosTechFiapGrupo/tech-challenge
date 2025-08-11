from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.cliente import ClienteEntity
from app.domain.events.cliente import (
    ClienteCreatedEvent,
    ClienteUpdatedEvent,
    ClienteDeletedEvent,
)
from app.domain.repositories.cliente import ClienteRepository


class ClienteUseCases(ABC):

    @abstractmethod
    def __init__(
        self,
        cliente_repository: ClienteRepository,
        cliente_created_event: ClienteCreatedEvent,
        cliente_updated_event: ClienteUpdatedEvent,
        cliente_deleted_event: ClienteDeletedEvent,
    ):
        self.cliente_repository = cliente_repository
        self.cliente_created_event = cliente_created_event
        self.cliente_updated_event = cliente_updated_event
        self.cliente_deleted_event = cliente_deleted_event

    @abstractmethod
    async def get_all_clientes(self) -> List[ClienteEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_cliente_by_id(self, id: str) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_cliente_by_cpf(self, cpf: str) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete_cliente(self, id: str) -> bool:
        raise NotImplementedError
