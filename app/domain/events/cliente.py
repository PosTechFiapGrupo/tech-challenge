from abc import ABC, abstractmethod
from app.domain.entities.cliente import ClienteEntity


class ClienteCreatedEvent(ABC):

    @abstractmethod
    def send(self, cliente: ClienteEntity) -> bool:
        raise NotImplementedError


class ClienteUpdatedEvent(ABC):

    @abstractmethod
    def send(self, cliente: ClienteEntity) -> bool:
        raise NotImplementedError


class ClienteDeletedEvent(ABC):

    @abstractmethod
    def send(self, cliente_id: str) -> bool:
        raise NotImplementedError
