from app.domain.exceptions import InvalidEmail, InvalidCPF, InvalidPhone
import re


class ClienteValidator:

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
