import pytest
from pydantic import ValidationError
from app.infrastructure.schemas.user_schema import UserCreate, UserOutput, UserFuncao

class TestUserSchemas:

    def test_user_create_valid(self):
        user = UserCreate(
            nome="Teste Usuario",
            email="teste@exemplo.com",  # String simples, não EmailStr()
            password="123456",
            funcao=UserFuncao.admin
        )
        assert user.nome == "Teste Usuario"
        assert user.email == "teste@exemplo.com"
        assert user.password == "123456"
        assert user.funcao == UserFuncao.admin

    def test_user_create_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(
                nome="Teste",
                email="email_invalido",  # inválido, deve disparar erro
                password="123456",
                funcao=UserFuncao.cliente
            )

    def test_user_output_attributes(self):
        user = UserOutput(
            id="1",
            nome="Nome Usuario",
            email="usuario@teste.com",  # string normal
            funcao=UserFuncao.cliente
        )
        assert user.id == "1"
        assert user.email == "usuario@teste.com"
        assert user.funcao == UserFuncao.cliente

    def test_user_update_password_validation(self):
        from app.infrastructure.schemas.user_schema import UserUpdate

        # senha menor que 8 caracteres deve falhar
        with pytest.raises(ValidationError):
            UserUpdate(password="1234567")

        # senha None (não obrigatória) deve passar
        update = UserUpdate(password=None)
        assert update.password is None

        # senha válida deve passar
        update = UserUpdate(password="12345678")
        assert update.password == "12345678"
