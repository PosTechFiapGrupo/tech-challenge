from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import UserEntity

class UserRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[UserEntity]:
        raise NotImplemented
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        raise NotImplemented
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        raise NotImplemented

    @abstractmethod
    async def add(self, user: UserEntity) -> UserEntity:
        raise NotImplemented
    
    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        raise NotImplemented

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        raise NotImplemented

