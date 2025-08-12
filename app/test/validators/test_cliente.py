import pytest
import re
from unittest.mock import AsyncMock
from app.domain.exceptions import InvalidEmail, InvalidCPF, InvalidPhone, ClienteNotFound
from app.application.validators.cliente import ClienteValidator


@pytest.mark.asyncio
class TestClienteValidator:

    @pytest.fixture
    def mock_repo(self):
        repo = AsyncMock()
        return repo

    @pytest.fixture
    def validator(self, mock_repo):
        return ClienteValidator(mock_repo)

    # validate_exists
    async def test_validate_exists_success(self, validator, mock_repo):
        mock_repo.get_by_id.return_value = {"id": "cli-1"}
        await validator.validate_exists("cli-1")
        mock_repo.get_by_id.assert_awaited_once_with("cli-1")

    async def test_validate_exists_raises_value_error_on_empty_id(self, validator):
        with pytest.raises(ValueError, match="ID do cliente é obrigatório"):
            await validator.validate_exists("")

    async def test_validate_exists_raises_cliente_not_found(self, validator, mock_repo):
        mock_repo.get_by_id.return_value = None
        with pytest.raises(ClienteNotFound):
            await validator.validate_exists("cli-999")

    # validate_email
    @pytest.mark.parametrize("email", [
        "teste@dominio.com",
        "usuario+teste@exemplo.org",
        "user.name@company.co.uk",
        None,
        ""
    ])
    def test_validate_email_valid(self, email):
        # Não deve lançar exceção para emails válidos ou vazios
        ClienteValidator.validate_email(email)

    @pytest.mark.parametrize("email", [
        "teste@@dominio.com",
        "teste.com",
        "user@domain",
        "user@domain.",
        "@domain.com",
        "user@.com",
        "user@domain.c",
    ])
    def test_validate_email_invalid(self, email):
        with pytest.raises(InvalidEmail):
            ClienteValidator.validate_email(email)

    # validate_cpf
    @pytest.mark.parametrize("cpf", [
        "123.456.789-09",
        "12345678909",
        "11122233344",
        None,
        ""
    ])
    def test_validate_cpf_valid(self, cpf):
        # Não deve lançar exceção para cpf válidos ou vazios
        ClienteValidator.validate_cpf(cpf)

    @pytest.mark.parametrize("cpf", [
        "123",
        "1234567890",  # 10 digits
        "123456789012",  # 12 digits
        "abc.def.ghi-jk",
    ])
    def test_validate_cpf_invalid(self, cpf):
        with pytest.raises(InvalidCPF):
            ClienteValidator.validate_cpf(cpf)

    # validate_phone
    @pytest.mark.parametrize("phone", [
        "11999999999",
        "(11) 99999-9999",
        "11 9999 9999",
        "+55 11 99999-9999",
        None,
        ""
    ])
    def test_validate_phone_valid(self, phone):
        # Não deve lançar exceção para telefone válidos ou vazios
        ClienteValidator.validate_phone(phone)

    @pytest.mark.parametrize("phone", [
        "1234",
        "123456789",  # 9 digits only
        "phone12345",
    ])
    def test_validate_phone_invalid(self, phone):
        with pytest.raises(InvalidPhone):
            ClienteValidator.validate_phone(phone)

    # validate_nome
    @pytest.mark.parametrize("nome", [
        "João Silva",
        " Ana ",
        "a" * 100,
    ])
    def test_validate_nome_valid(self, nome):
        ClienteValidator.validate_nome(nome)

    @pytest.mark.parametrize("nome", [
        None,
        "",
        "   ",
    ])
    def test_validate_nome_empty(self, nome):
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            ClienteValidator.validate_nome(nome)

    def test_validate_nome_too_long(self):
        with pytest.raises(ValueError, match="Nome deve ter no máximo 100 caracteres"):
            ClienteValidator.validate_nome("a" * 101)
