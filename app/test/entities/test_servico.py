import pytest
from app.domain.entities.servico import ServicoEntity, ServicoEntityFactory
from app.domain.exceptions import PriceIsLessThanOrEqualToZero, InvalidDescription


class TestServicoEntity:

    def test_create_servico_with_valid_data(self):
        servico = ServicoEntity("1", "Consultoria em TI", 150.00)
        assert servico.id == "1"
        assert servico.descricao == "Consultoria em TI"
        assert servico.preco == 150.00

    def test_create_servico_with_zero_price(self):
        with pytest.raises(PriceIsLessThanOrEqualToZero):
            ServicoEntity("1", "Consultoria em TI", 0.00)

    def test_create_servico_with_negative_price(self):
        with pytest.raises(PriceIsLessThanOrEqualToZero):
            ServicoEntity("1", "Consultoria em TI", -10.00)

    def test_create_servico_with_empty_description(self):
        with pytest.raises(InvalidDescription):
            ServicoEntity("1", "", 150.00)

    def test_create_servico_with_whitespace_description(self):
        with pytest.raises(InvalidDescription):
            ServicoEntity("1", "   ", 150.00)


class TestServicoEntityFactory:

    def test_create_servico_with_id(self):
        servico = ServicoEntityFactory.create("1", "Consultoria em TI", 150.00)
        assert servico.id == "1"
        assert servico.descricao == "Consultoria em TI"
        assert servico.preco == 150.00

    def test_create_servico_without_id_generates_uuid(self):
        servico = ServicoEntityFactory.create(None, "Consultoria em TI", 150.00)
        assert servico.id is not None
        assert len(servico.id) == 36  # UUID length

    def test_create_servico_converts_price_to_float(self):
        servico = ServicoEntityFactory.create("1", "Consultoria em TI", "150.50")
        assert servico.preco == 150.50
        assert isinstance(servico.preco, float)
