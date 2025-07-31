import pytest
from app.domain.entities.cliente import ClienteEntity, ClienteEntityFactory
from app.domain.exceptions import InvalidEmail, InvalidCPF, InvalidPhone


class TestClienteEntity:

    def test_create_cliente_with_valid_data(self):
        cliente = ClienteEntity(
            "1", "João Silva", "11999999999", "joao@email.com", "12345678901"
        )
        assert cliente.id == "1"
        assert cliente.nome == "João Silva"
        assert cliente.telefone == "11999999999"
        assert cliente.email == "joao@email.com"
        assert cliente.cpf == "12345678901"

    def test_create_cliente_with_invalid_email(self):
        with pytest.raises(InvalidEmail):
            ClienteEntity(
                "1", "João Silva", "11999999999", "email_invalido", "12345678901"
            )

    def test_create_cliente_with_invalid_cpf(self):
        with pytest.raises(InvalidCPF):
            ClienteEntity("1", "João Silva", "11999999999", "joao@email.com", "123")

    def test_create_cliente_with_invalid_phone(self):
        with pytest.raises(InvalidPhone):
            ClienteEntity("1", "João Silva", "123", "joao@email.com", "12345678901")

    def test_create_cliente_with_optional_fields_none(self):
        cliente = ClienteEntity("1", "João Silva")
        assert cliente.id == "1"
        assert cliente.nome == "João Silva"
        assert cliente.telefone is None
        assert cliente.email is None
        assert cliente.cpf is None


class TestClienteEntityFactory:

    def test_create_cliente_with_id(self):
        cliente = ClienteEntityFactory.create(
            "1", "João Silva", "11999999999", "joao@email.com", "12345678901"
        )
        assert cliente.id == "1"
        assert cliente.nome == "João Silva"

    def test_create_cliente_without_id_generates_uuid(self):
        cliente = ClienteEntityFactory.create(
            None, "João Silva", "11999999999", "joao@email.com", "12345678901"
        )
        assert cliente.id is not None
        assert len(cliente.id) == 36  # UUID length
