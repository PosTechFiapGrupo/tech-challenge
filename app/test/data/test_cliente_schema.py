import pytest
from pydantic import ValidationError, EmailStr
from app.infrastructure.schemas.cliente import ClienteInput, ClienteUpdate

class TestClienteSchemas:

    def test_cliente_input_valid_minimal(self):
        data = ClienteInput(nome="João Silva")
        assert data.nome == "João Silva"
        assert data.email is None
        assert data.cpf is None
        assert data.telefone is None

    def test_cliente_input_valid_all_fields(self):
        data = ClienteInput(
            nome="Maria Oliveira",
            telefone="(11) 91234-5678",
            email="maria@example.com",
            cpf="123.456.789-00"
        )
        assert data.nome == "Maria Oliveira"
        assert data.email == "maria@example.com"
        assert data.cpf == "123.456.789-00"

    def test_cliente_input_nome_required(self):
        with pytest.raises(ValidationError):
            ClienteInput(nome="")  # nome vazio

    def test_cliente_input_nome_too_long(self):
        with pytest.raises(ValidationError):
            ClienteInput(nome="a" * 101)  # > 100 caracteres

    def test_cliente_input_cpf_invalid_length(self):
        with pytest.raises(ValidationError):
            ClienteInput(nome="Teste", cpf="123")  # cpf com menos de 11 dígitos

    def test_cliente_input_telefone_invalid_length(self):
        with pytest.raises(ValidationError):
            ClienteInput(nome="Teste", telefone="12345")  # telefone com menos de 10 dígitos

    def test_cliente_input_email_invalid(self):
        with pytest.raises(ValidationError):
            ClienteInput(nome="Teste", email="email-invalido")

    def test_cliente_update_valid(self):
        data = ClienteUpdate(nome="Novo Nome", telefone="11987654321")
        assert data.nome == "Novo Nome"
        assert data.telefone == "11987654321"

    def test_cliente_update_nome_empty(self):
        with pytest.raises(ValidationError):
            ClienteUpdate(nome="  ")  # nome vazio

    def test_cliente_update_cpf_invalid(self):
        with pytest.raises(ValidationError):
            ClienteUpdate(cpf="111222")  # cpf inválido

    def test_cliente_update_telefone_invalid(self):
        with pytest.raises(ValidationError):
            ClienteUpdate(telefone="123")  # telefone inválido
