from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum

class UserFuncao(str, Enum):
    admin= "admin"
    cliente = "cliente"
    mecanico = "mecanico"
    atendente = "atendente"

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    funcao: UserFuncao

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        if len(v) > 255:
            raise ValueError("Nome deve ter no máximo 255 caracteres")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        return v

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    funcao: Optional[UserFuncao] = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("Nome não pode ser vazio")
            if len(v) > 255:
                raise ValueError("Nome deve ter no máximo 255 caracteres")
            return v.strip()
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError("Senha deve ter pelo menos 8 caracteres")
            return v
        return v

class UserOutput(BaseModel):
    id: str
    nome: str
    email: EmailStr
    funcao: UserFuncao

    class Config:
        orm_mode = True
