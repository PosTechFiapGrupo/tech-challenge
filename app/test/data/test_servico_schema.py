import pytest
from pydantic import ValidationError
from app.infrastructure.schemas.servico import ServicoInput, ServicoOutput, ServicoUpdate

class TestServicoSchemas:

    def test_servico_input_valid(self):
        data = ServicoInput(descricao="Serviço Teste", preco=150.50)
        assert data.descricao == "Serviço Teste"
        assert data.preco == 150.50

    def test_servico_input_invalid_descricao(self):
        with pytest.raises(ValidationError):
            ServicoInput(descricao="", preco=10.0)
        with pytest.raises(ValidationError):
            ServicoInput(descricao=" " * 300, preco=10.0)  # Muito longo

    def test_servico_input_invalid_preco(self):
        with pytest.raises(ValidationError):
            ServicoInput(descricao="Serviço", preco=0)
        with pytest.raises(ValidationError):
            ServicoInput(descricao="Serviço", preco=-5)

    def test_servico_output_attributes(self):
        data = ServicoOutput(id="abc123", descricao="Servico", preco=20.0)
        assert data.id == "abc123"
        assert data.descricao == "Servico"
        assert data.preco == 20.0

    def test_servico_update_valid(self):
        data = ServicoUpdate(descricao="Atualizado", preco=50.5)
        assert data.descricao == "Atualizado"
        assert data.preco == 50.5

        data_none = ServicoUpdate()
        assert data_none.descricao is None
        assert data_none.preco is None

    def test_servico_update_invalid_descricao(self):
        with pytest.raises(ValidationError):
            ServicoUpdate(descricao="")
        with pytest.raises(ValidationError):
            ServicoUpdate(descricao=" " * 300)

    def test_servico_update_invalid_preco(self):
        with pytest.raises(ValidationError):
            ServicoUpdate(preco=0)
        with pytest.raises(ValidationError):
            ServicoUpdate(preco=-10)
