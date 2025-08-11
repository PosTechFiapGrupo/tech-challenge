import pytest
from datetime import datetime
from app.domain.entities.user import UserEntity, UserEntityFactory, UserFuncao
from app.domain.exceptions import InvalidName, InvalidEmail, InvalidPassword


class TestUserEntity:

    def test_create_user_with_valid_data(self):
        user = UserEntity(
            "1",
            "João da Silva",
            "joao@example.com",
            "hashed_senha123",
            UserFuncao.CLIENTE,
        )
        assert user.id == "1"
        assert user.nome == "João da Silva"
        assert user.email == "joao@example.com"
        assert user.hashed_password == "hashed_senha123"
        assert user.funcao == UserFuncao.CLIENTE

    def test_create_user_with_invalid_name_empty(self):
        with pytest.raises(InvalidName):
            UserEntity("1", "", "joao@example.com", "senha12345", UserFuncao.CLIENTE)

    def test_create_user_with_invalid_name_short(self):
        with pytest.raises(InvalidName):
            UserEntity("1", "Jo", "joao@example.com", "senha12345", UserFuncao.CLIENTE)

    def test_create_user_with_invalid_email_missing_at(self):
        with pytest.raises(InvalidEmail):
            UserEntity("1", "João da Silva", "joaoexample.com", "senha12345", UserFuncao.CLIENTE)

    def test_create_user_with_invalid_email_empty(self):
        with pytest.raises(InvalidEmail):
            UserEntity("1", "João da Silva", "", "senha12345", UserFuncao.CLIENTE)

    def test_create_user_with_short_password(self):
        with pytest.raises(InvalidPassword):
            UserEntity("1", "João da Silva", "joao@example.com", "short", UserFuncao.CLIENTE)

    def test_create_user_with_empty_password(self):
        with pytest.raises(InvalidPassword):
            UserEntity("1", "João da Silva", "joao@example.com", "", UserFuncao.CLIENTE)


class TestUserEntityFactory:

    def test_create_user_with_id(self):
        user = UserEntityFactory.create(
            "1",
            "Maria Souza",
            "maria@example.com",
            "hashed_abc12345",
            UserFuncao.MECANICO,
        )
        assert user.id == "1"
        assert user.nome == "Maria Souza"
        assert user.email == "maria@example.com"
        assert user.hashed_password == "hashed_abc12345"
        assert user.funcao == UserFuncao.MECANICO

    def test_create_user_without_id_generates_uuid(self):
        user = UserEntityFactory.create(
            None,
            "Carlos Alberto",
            "carlos@example.com",
            "hashed_senha123",
            UserFuncao.ATENDENTE,
        )
        assert user.id is not None
        assert len(user.id) == 36  # UUID format

    def test_create_user_with_dates(self):
        criado_em = datetime.now()
        atualizado_em = datetime.now()
        user = UserEntityFactory.create(
            "1",
            "Pedro Lima",
            "pedro@example.com",
            "hashed_abc12345",
            UserFuncao.CLIENTE,
            criado_em,
            atualizado_em,
        )
        assert user.criado_em == criado_em
        assert user.atualizado_em == atualizado_em
