import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.application.validators.ordem_servico import OrdemServicoValidator
from app.domain.entities.status_ordem_servico import StatusOrdemServico


@pytest.mark.asyncio
class TestOrdemServicoValidator:

    @pytest.fixture
    def mock_cliente_repo(self):
        return AsyncMock()

    @pytest.fixture
    def mock_servico_repo(self):
        return AsyncMock()

    @pytest.fixture
    def validator(self, mock_cliente_repo, mock_servico_repo):
        return OrdemServicoValidator(
            cliente_repository=mock_cliente_repo,
            servico_repository=mock_servico_repo,
        )

    async def test_validate_cliente_exists_success(self, validator, mock_cliente_repo):
        mock_cliente_repo.get_by_id.return_value = {"id": "cli-1"}
        await validator.validate_cliente_exists("cli-1")
        mock_cliente_repo.get_by_id.assert_awaited_once_with("cli-1")

    async def test_validate_cliente_exists_not_found(self, validator, mock_cliente_repo):
        mock_cliente_repo.get_by_id.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await validator.validate_cliente_exists("cli-999")
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente não encontrado"

    async def test_validate_servicos_exist_all_exist(self, validator, mock_servico_repo):
        mock_servico_repo.get_by_id.side_effect = lambda sid: {"id": sid}
        await validator.validate_servicos_exist(["s1", "s2"])
        assert mock_servico_repo.get_by_id.call_count == 2
        mock_servico_repo.get_by_id.assert_any_await("s1")
        mock_servico_repo.get_by_id.assert_any_await("s2")

    async def test_validate_servicos_exist_not_found(self, validator, mock_servico_repo):
        async def get_by_id(sid):
            if sid == "s2":
                return None
            return {"id": sid}
        mock_servico_repo.get_by_id.side_effect = get_by_id

        with pytest.raises(HTTPException) as exc_info:
            await validator.validate_servicos_exist(["s1", "s2", "s3"])
        assert exc_info.value.status_code == 404
        assert "Serviço s2 não encontrado" in exc_info.value.detail

    @pytest.mark.parametrize(
        "current,new,raises",
        [
            (StatusOrdemServico.RECEBIDA, StatusOrdemServico.EM_DIAGNOSTICO, False),
            (StatusOrdemServico.EM_DIAGNOSTICO, StatusOrdemServico.AGUARDANDO_APROVACAO, False),
            (StatusOrdemServico.AGUARDANDO_APROVACAO, StatusOrdemServico.EM_EXECUCAO, False),
            (StatusOrdemServico.AGUARDANDO_APROVACAO, StatusOrdemServico.CANCELADA, False),
            (StatusOrdemServico.EM_EXECUCAO, StatusOrdemServico.FINALIZADA, False),
            (StatusOrdemServico.FINALIZADA, StatusOrdemServico.ENTREGUE, False),
            # Invalid transitions
            (StatusOrdemServico.RECEBIDA, StatusOrdemServico.CANCELADA, True),
            (StatusOrdemServico.FINALIZADA, StatusOrdemServico.RECEBIDA, True),
            (StatusOrdemServico.EM_DIAGNOSTICO, StatusOrdemServico.FINALIZADA, True),
            (StatusOrdemServico.AGUARDANDO_APROVACAO, StatusOrdemServico.FINALIZADA, True),
        ],
    )
    def test_validate_status_transition(self, current, new, raises):
        if raises:
            with pytest.raises(HTTPException) as exc_info:
                OrdemServicoValidator.validate_status_transition(current, new)
            assert exc_info.value.status_code == 400
            assert "Transição inválida de status" in exc_info.value.detail
        else:
            OrdemServicoValidator.validate_status_transition(current, new)
