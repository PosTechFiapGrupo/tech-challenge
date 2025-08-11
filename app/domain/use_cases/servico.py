from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.servico import ServicoEntity
from app.domain.events.servico import (
    ServicoCreatedEvent,
    ServicoUpdatedEvent,
    ServicoDeletedEvent,
)
from app.domain.repositories.servico import ServicoRepository


class ServicoUseCases(ABC):

    @abstractmethod
    def __init__(
        self,
        servico_repository: ServicoRepository,
        servico_created_event: ServicoCreatedEvent,
        servico_updated_event: ServicoUpdatedEvent,
        servico_deleted_event: ServicoDeletedEvent,
    ):
        self.servico_repository = servico_repository
        self.servico_created_event = servico_created_event
        self.servico_updated_event = servico_updated_event
        self.servico_deleted_event = servico_deleted_event

    @abstractmethod
    async def get_all_servicos(self) -> List[ServicoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_servico_by_id(self, id: str) -> ServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_servico(self, servico: ServicoEntity) -> ServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_servico(self, servico: ServicoEntity) -> ServicoEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete_servico(self, id: str) -> bool:
        raise NotImplementedError
