from app.domain.exceptions import InvalidEmail
import re

class UserValidator:

    @staticmethod
    def validate_email(email: str) -> None:
        if email:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, email):
                raise InvalidEmail

    @staticmethod
    def validate_nome(nome: str) -> None:
        if not nome or len(nome.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        if len(nome) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")

    @staticmethod
    def validate_funcao(funcao: str) -> None:
        if not funcao or len(funcao.strip()) == 0:
            raise ValueError("Função é obrigatória")
        if len(funcao) > 100:
            raise ValueError("Função deve ter no máximo 100 caracteres")
        
    @staticmethod
    def validate_password(password: str) -> None:
        if not password or len(password.strip()) == 0:
            raise ValueError("Senha é obrigatória")
        password = password.strip()  # Remove espaços das bordas antes de validar tamanho
        if len(password) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")