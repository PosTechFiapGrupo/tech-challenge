import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.application.validators.servico import ServicoValidator
from app.domain.exceptions import ServicoNotFound, PriceIsLessThanOrEqualToZero, InvalidPrice


@pytest.mark.asyncio
class TestServicoValidator:

    @pytest.fixture
    def mock_repo(self):
        return AsyncMock()

    @pytest.fixture
    def validator(self, mock_repo):
        return ServicoValidator(mock_repo)

    # Testa o método validate_exists para uma lista de 1 elemento (simulando único)
    async def test_validate_exists_single_success(self, validator, mock_repo):
        mock_repo.get_by_id.return_value = {"id": "s1"}
        await validator.validate_exists(["s1"])  # passar lista com um id
        mock_repo.get_by_id.assert_awaited_once_with("s1")

    async def test_validate_exists_single_not_found(self, validator, mock_repo):
        mock_repo.get_by_id.return_value = None
        with pytest.raises(ServicoNotFound):
            await validator.validate_exists(["s999"])

    # Testa o método para lista de vários IDs
    async def test_validate_exists_list_success(self, validator, mock_repo):
        mock_repo.get_by_id.side_effect = lambda sid: {"id": sid}
        await validator.validate_exists(["s1", "s2"])
        assert mock_repo.get_by_id.await_count == 2

    async def test_validate_exists_list_empty(self, validator):
        with pytest.raises(ValueError, match="Lista de IDs de serviços é obrigatória"):
            await validator.validate_exists([])

    async def test_validate_exists_list_missing_service(self, validator, mock_repo):
        async def get_by_id(sid):
            return None if sid == "s2" else {"id": sid}
        mock_repo.get_by_id.side_effect = get_by_id

        with pytest.raises(ServicoNotFound) as exc_info:
            await validator.validate_exists(["s1", "s2"])
        assert "s2" in str(exc_info.value)

    def test_validate_preco_zero_or_negative(self):
        with pytest.raises(PriceIsLessThanOrEqualToZero):
            ServicoValidator.validate_preco(0)
        with pytest.raises(PriceIsLessThanOrEqualToZero):
            ServicoValidator.validate_preco(-5)

    # Testa validação de descrição
    def test_validate_descricao_valid(self):
        ServicoValidator.validate_descricao("Descrição válida")
        ServicoValidator.validate_descricao(" " * 10 + "Texto" + " " * 5)

    def test_validate_descricao_empty_or_none(self):
        with pytest.raises(ValueError):
            ServicoValidator.validate_descricao("")
        with pytest.raises(ValueError):
            ServicoValidator.validate_descricao("   ")

    def test_validate_descricao_too_long(self):
        with pytest.raises(ValueError):
            ServicoValidator.validate_descricao("a" * 256)
