from app.domain.exceptions import InvalidPrice, PriceIsLessThanOrEqualToZero
from app.domain.repositories.servico import ServicoRepository
from fastapi import HTTPException


class ServicoValidator:
    def __init__(self, repository: ServicoRepository):
        self.repository = repository

    async def validate_exists(self, id: str) -> None:
        if await self.repository.get_by_id(id) is None:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

    @staticmethod
    def validate_preco(preco: float) -> float:
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                raise PriceIsLessThanOrEqualToZero
            return preco_float
        except ValueError:
            raise InvalidPrice

    @staticmethod
    def validate_descricao(descricao: str) -> None:
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição é obrigatória")
        if len(descricao) > 255:
            raise ValueError("Descrição deve ter no máximo 255 caracteres")
