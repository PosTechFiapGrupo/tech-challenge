from pydantic import BaseModel, field_validator
from typing import Optional


class ServicoInput(BaseModel):
    descricao: str
    preco: float

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Descrição é obrigatória")
        if len(v) > 255:
            raise ValueError("Descrição deve ter no máximo 255 caracteres")
        return v.strip()

    @field_validator("preco")
    @classmethod
    def validate_preco(cls, v):
        if v <= 0:
            raise ValueError("Preço deve ser maior que zero")
        return round(float(v), 2)


class ServicoOutput(BaseModel):
    id: str
    descricao: str
    preco: float


class ServicoUpdate(BaseModel):
    descricao: Optional[str] = None
    preco: Optional[float] = None

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("Descrição não pode ser vazia")
            if len(v) > 255:
                raise ValueError("Descrição deve ter no máximo 255 caracteres")
            return v.strip()
        return v

    @field_validator("preco")
    @classmethod
    def validate_preco(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Preço deve ser maior que zero")
            return round(float(v), 2)
        return v
