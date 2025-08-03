from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
import re


class ClienteInput(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        if len(v) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
        return v.strip()

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v):
        if v:
            cpf_numbers = re.sub(r"[^0-9]", "", v)
            if len(cpf_numbers) != 11:
                raise ValueError("CPF deve ter 11 dígitos")
        return v

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, v):
        if v:
            phone_numbers = re.sub(r"[^0-9]", "", v)
            if len(phone_numbers) < 10:
                raise ValueError("Telefone deve ter pelo menos 10 dígitos")
        return v


class ClienteOutput(BaseModel):
    id: str
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("Nome não pode ser vazio")
            if len(v) > 100:
                raise ValueError("Nome deve ter no máximo 100 caracteres")
            return v.strip()
        return v

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v):
        if v:
            cpf_numbers = re.sub(r"[^0-9]", "", v)
            if len(cpf_numbers) != 11:
                raise ValueError("CPF deve ter 11 dígitos")
        return v

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, v):
        if v:
            phone_numbers = re.sub(r"[^0-9]", "", v)
            if len(phone_numbers) < 10:
                raise ValueError("Telefone deve ter pelo menos 10 dígitos")
        return v
