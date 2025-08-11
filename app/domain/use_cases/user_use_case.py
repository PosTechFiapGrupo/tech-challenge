from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.user import UserEntity
from app.domain.events.user_event import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent,
)
from app.domain.repositories.user_repository import UserRepository
from app.application.services.password_service import PasswordService


class UserUseCases(ABC):

    @abstractmethod
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        user_created_event: UserCreatedEvent,
        user_updated_event: UserUpdatedEvent,
        user_deleted_event: UserDeletedEvent,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.user_created_event = user_created_event
        self.user_updated_event = user_updated_event
        self.user_deleted_event = user_deleted_event

    @abstractmethod
    async def get_all_users(self) -> List[UserEntity]:
        raise NotImplemented

    @abstractmethod
    async def get_user_by_id(self, id: int) -> UserEntity:
        raise NotImplemented
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserEntity:
        raise NotImplemented

    @abstractmethod
    async def create_user(self, user: UserEntity, plain_password: str) -> UserEntity:
        raise NotImplemented

    @abstractmethod
    async def update_user(self, user: UserEntity) -> UserEntity:
        raise NotImplemented

    @abstractmethod
    async def delete_user(self, id: int) -> bool:
        raise NotImplemented