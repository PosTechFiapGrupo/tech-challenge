import pytest
from app.application.validators.user_validator import UserValidator
from app.domain.exceptions import InvalidEmail

class TestUserValidator:

    # validate_email

    def test_validate_email_valid(self):
        valid_emails = [
            "user@example.com",
            "user.name+tag+sorting@example.com",
            "user_name@example.co.uk",
            "user-name@example.io",
        ]
        for email in valid_emails:
            UserValidator.validate_email(email)  # não deve levantar exceção

    def test_validate_email_empty_or_none(self):
        # Deve permitir email vazio ou None sem exceção
        UserValidator.validate_email("")
        UserValidator.validate_email(None)

    # validate_nome

    def test_validate_nome_valid(self):
        UserValidator.validate_nome("Nome Válido")
        UserValidator.validate_nome(" A " * 30)  # até 100 chars ok

    def test_validate_nome_empty(self):
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            UserValidator.validate_nome("")
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            UserValidator.validate_nome("   ")

    def test_validate_nome_too_long(self):
        with pytest.raises(ValueError, match="Nome deve ter no máximo 100 caracteres"):
            UserValidator.validate_nome("a" * 101)

    # validate_funcao

    def test_validate_funcao_valid(self):
        UserValidator.validate_funcao("Administrador")
        UserValidator.validate_funcao(" A " * 30)  # até 100 chars ok

    def test_validate_funcao_empty(self):
        with pytest.raises(ValueError, match="Função é obrigatória"):
            UserValidator.validate_funcao("")
        with pytest.raises(ValueError, match="Função é obrigatória"):
            UserValidator.validate_funcao("   ")

    def test_validate_funcao_too_long(self):
        with pytest.raises(ValueError, match="Função deve ter no máximo 100 caracteres"):
            UserValidator.validate_funcao("a" * 101)

    # validate_password

    def test_validate_password_valid(self):
        UserValidator.validate_password("password123")
        UserValidator.validate_password("   senhaComEspacos   ")

    def test_validate_password_empty(self):
        with pytest.raises(ValueError, match="Senha é obrigatória"):
            UserValidator.validate_password("")
        with pytest.raises(ValueError, match="Senha é obrigatória"):
            UserValidator.validate_password("    ")

    def test_validate_password_too_short(self):
        with pytest.raises(ValueError, match="Senha deve ter no mínimo 8 caracteres"):
            UserValidator.validate_password("1234567")
        with pytest.raises(ValueError, match="Senha deve ter no mínimo 8 caracteres"):
            UserValidator.validate_password("  1234  ")  # espaços removidos, fica menor que 8
