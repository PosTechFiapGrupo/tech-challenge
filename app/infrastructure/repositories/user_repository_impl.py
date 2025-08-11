from typing import List
from sqlalchemy import select, update, delete, func
from app.domain.entities.user import UserEntity, UserEntityFactory
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.database import database


class UserRepositoryImpl(UserRepository):

    def __init__(self):
        self.database = database

    async def get_all(self) -> List[UserEntity]:
        async for session in self.database.get_session():
            stmt = select(UserModel)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return [
                UserEntityFactory.create(
                    id=str(user.id),
                    nome=user.nome,
                    email=user.email,
                    hashed_password=user.hashed_password,
                    funcao=user.funcao,
                    criado_em=user.criado_em,
                    atualizado_em=user.atualizado_em
                )
                for user in users
            ]

    async def get_by_id(self, id: str) -> UserEntity | None:
        async for session in self.database.get_session():
            stmt = select(UserModel).where(UserModel.id == id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return UserEntityFactory.create(
                id=str(user.id),
                nome=user.nome,
                email=user.email,
                hashed_password=user.hashed_password,
                funcao=user.funcao,
                criado_em=user.criado_em,
                atualizado_em=user.atualizado_em
            )

    async def get_by_email(self, email: str) -> UserEntity | None:
        email = email.lower().strip()
        async for session in self.database.get_session():
            stmt = select(UserModel).where(func.lower(UserModel.email) == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                return None

            return UserEntityFactory.create(
                id=str(user.id),
                nome=user.nome,
                email=user.email,
                hashed_password=user.hashed_password,
                funcao=user.funcao,
                criado_em=user.criado_em,
                atualizado_em=user.atualizado_em
            )

    async def add(self, user: UserEntity) -> UserEntity:
        async for session in self.database.get_session():
            user_model = UserModel(
                nome=user.nome,
                email=user.email,
                hashed_password=user.hashed_password,
                funcao=user.funcao,
            )
            session.add(user_model)
            await session.flush()
            await session.refresh(user_model)
            await session.commit()

            user.id = str(user_model.id)
            return user

    async def update(self, user: UserEntity) -> UserEntity:
        async for session in self.database.get_session():
            stmt = update(UserModel).where(UserModel.id == user.id).values(
                nome=user.nome,
                email=user.email,
                hashed_password=user.hashed_password,
                funcao=user.funcao
            )
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise ValueError(f"User with id {user.id} not found")
            await session.commit()
            return user

    async def delete(self, id: str) -> bool:
        async for session in self.database.get_session():
            stmt = delete(UserModel).where(UserModel.id == id)
            result = await session.execute(stmt)
            success = result.rowcount > 0
            if success:
                await session.commit()
            return success
