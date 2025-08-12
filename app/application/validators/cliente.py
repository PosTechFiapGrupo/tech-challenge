import re

from app.domain.exceptions import InvalidEmail, InvalidCPF, InvalidPhone, ClienteNotFound
from app.domain.repositories.cliente import ClienteRepository



class ClienteValidator:

    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    async def validate_exists(self, cliente_id: str) -> None:
        """Valida se o cliente existe"""
        if not cliente_id:
            raise ValueError("ID do cliente é obrigatório")
        
        cliente = await self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ClienteNotFound(f"Cliente com ID '{cliente_id}' não encontrado")

    @staticmethod
    def validate_email(email: str) -> None:
        if email:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, email):
                raise InvalidEmail

    @staticmethod
    def validate_cpf(cpf: str) -> None:
        if cpf:
            # Remove caracteres especiais
            cpf_numbers = re.sub(r"[^0-9]", "", cpf)
            if len(cpf_numbers) != 11:
                raise InvalidCPF

    @staticmethod
    def validate_phone(telefone: str) -> None:
        if telefone:
            # Remove caracteres especiais
            phone_numbers = re.sub(r"[^0-9]", "", telefone)
            if len(phone_numbers) < 10:
                raise InvalidPhone

    @staticmethod
    def validate_nome(nome: str) -> None:
        if not nome or len(nome.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        if len(nome) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
