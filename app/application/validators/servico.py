from app.domain.exceptions import InvalidPrice, PriceIsLessThanOrEqualToZero, ServicoNotFound
from app.domain.repositories.servico import ServicoRepository
from fastapi import HTTPException


class ServicoValidator:
    def __init__(self, repository: ServicoRepository):
        self.repository = repository

    async def validate_exists(self, id: str) -> None:
        if await self.repository.get_by_id(id) is None:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

    async def validate_exists(self, servico_ids: list[str]) -> None:
        """Valida se todos os serviços existem"""
        if not servico_ids:
            raise ValueError("Lista de IDs de serviços é obrigatória")
        
        for servico_id in servico_ids:
            servico = await self.repository.get_by_id(servico_id)
            if not servico:
                raise ServicoNotFound(f"Serviço com ID '{servico_id}' não encontrado")

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
