from typing import List, Optional

from app.application.services.password_service import PasswordService
from app.application.validators.user_validator import UserValidator
from app.domain.entities.user import UserEntity
from app.domain.events.user_event import (
    UserCreatedEvent,
    UserDeletedEvent,
    UserUpdatedEvent,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.user_use_case import UserUseCases
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class UserService(UserUseCases):

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        user_created_event: UserCreatedEvent,
        user_updated_event: UserUpdatedEvent,
        user_deleted_event: UserDeletedEvent,
    ):
        super().__init__(
            user_repository, 
            password_service,
            user_created_event,
            user_updated_event,
            user_deleted_event
        )
        

    async def get_all_users(self) -> List[UserEntity]:
        users = await self.user_repository.get_all()
        logger.info("Usuários listados", extra={"count": len(users)})
        return users

    async def get_user_by_id(self, user_id: str) -> Optional[UserEntity]:
        user = await self.user_repository.get_by_id(user_id)
        logger.info("Usuário buscado por ID", extra={"user_id": user_id, "found": user is not None})
        return user

    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        email = email.lower().strip()
        user = await self.user_repository.get_by_email(email)
        logger.info("Usuário buscado por email", extra={"found": user is not None})
        return user

    async def create_user(self, user: UserEntity, plain_password: str) -> UserEntity:
        UserValidator.validate_nome(user.nome)
        UserValidator.validate_email(user.email)
        UserValidator.validate_funcao(user.funcao)
        UserValidator.validate_password(plain_password)

        user.hashed_password = self.password_service.hash_password(plain_password)
        created_user = await self.user_repository.add(user)
        self.user_created_event.send(created_user)
        logger.info("Usuário criado", extra={"user_id": str(created_user.id), "funcao": user.funcao})
        return created_user

    async def update_user(self, user: UserEntity) -> UserEntity:
        UserValidator.validate_nome(user.nome)
        UserValidator.validate_email(user.email)
        UserValidator.validate_funcao(user.funcao)

        updated_user = await self.user_repository.update(user)
        self.user_updated_event.send(updated_user)
        logger.info("Usuário atualizado", extra={"user_id": str(user.id)})
        return updated_user

    async def delete_user(self, user_id: str) -> bool:
        result = await self.user_repository.delete(user_id)
        if result:
            self.user_deleted_event.send(user_id)
            logger.info("Usuário deletado", extra={"user_id": user_id})
        else:
            logger.warning("Falha ao deletar usuário", extra={"user_id": user_id})
        return result
