import uuid
from enum import Enum
from app.domain.exceptions import InvalidName, InvalidEmail, InvalidPassword
from datetime import datetime
from typing import Optional


class UserFuncao(str, Enum):
    ADMIN = "admin"
    CLIENTE = "cliente"
    MECANICO = "mecanico"
    ATENDENTE = "atendente"


class UserEntity:

    def __init__(self, uid: str, nome: str, email: str, hashed_password: str, funcao: UserFuncao, criado_em: Optional[datetime] = None, atualizado_em: Optional[datetime] = None):
        self.__validate_nome(nome)
        self.__validate_email(email)
        self.__validate_password(hashed_password)

        self.id = uid
        self.nome = nome
        self.email = email
        self.hashed_password = hashed_password
        self.funcao = funcao
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    @staticmethod
    def __validate_nome(nome: str):
        if not nome or len(nome.strip()) < 3:
            raise InvalidName

    @staticmethod
    def __validate_email(email: str):
        if not email or "@" not in email:
            raise InvalidEmail

    @staticmethod
    def __validate_password(password: str):
        if not password or len(password.strip()) < 8:
            raise InvalidPassword


class UserEntityFactory:

    @staticmethod
    def create(
        id: str | None, 
        nome: str, 
        email: str, 
        hashed_password: str, 
        funcao: UserFuncao, 
        criado_em: Optional[datetime] = None, 
        atualizado_em: Optional[datetime] = None,
    ) -> UserEntity:
        if id is None:
            id = uuid.uuid4().__str__()
        return UserEntity(
            id, 
            nome, 
            email, 
            hashed_password, 
            funcao,
            criado_em,
            atualizado_em,
        )
