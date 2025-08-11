from abc import ABC, abstractmethod
from app.domain.entities.user import UserEntity


class UserCreatedEvent(ABC):

    @abstractmethod
    def send(self, user: UserEntity) -> bool:
        raise NotImplemented


class UserUpdatedEvent(ABC):

    @abstractmethod
    def send(self, user: UserEntity) -> bool:
        raise NotImplemented


class UserDeletedEvent(ABC):

    @abstractmethod
    def send(self, user_id: str) -> bool:
        raise NotImplemented
