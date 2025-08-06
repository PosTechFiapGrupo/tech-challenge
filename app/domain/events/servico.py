from abc import ABC, abstractmethod
from app.domain.entities.servico import ServicoEntity


class ServicoCreatedEvent(ABC):

    @abstractmethod
    def send(self, servico: ServicoEntity) -> bool:
        raise NotImplementedError


class ServicoUpdatedEvent(ABC):

    @abstractmethod
    def send(self, servico: ServicoEntity) -> bool:
        raise NotImplementedError


class ServicoDeletedEvent(ABC):

    @abstractmethod
    def send(self, servico_id: str) -> bool:
        raise NotImplementedError
