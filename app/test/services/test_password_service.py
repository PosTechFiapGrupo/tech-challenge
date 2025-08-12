import pytest
from app.application.services.password_service import PasswordService

class TestPasswordService:

    def setup_method(self):
        self.service = PasswordService()

    def test_hash_password_gera_hash(self):
        senha = "minhaSenha123"
        hashed = self.service.hash_password(senha)
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != senha  # hash deve ser diferente da senha em texto puro

    def test_verify_password_valida_senha_correta(self):
        senha = "minhaSenha123"
        hashed = self.service.hash_password(senha)
        assert self.service.verify_password(senha, hashed) is True

    def test_verify_password_rejeita_senha_errada(self):
        senha = "minhaSenha123"
        hashed = self.service.hash_password(senha)
        assert self.service.verify_password("senhaErrada", hashed) is False
