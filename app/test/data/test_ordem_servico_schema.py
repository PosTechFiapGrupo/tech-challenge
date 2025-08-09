import pytest
from app.infrastructure.schemas.ordem_servico import (
    OrdemServicoInput,
    OrdemServicoUpdate,
)
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class TestOrdemServicoSchemas:

    def test_ordem_servico_input_valid(self):
        data = OrdemServicoInput(
            cliente_id="cli-1",
            vehicle_id=123,
            servico_ids=["s1", "s2"],
            status="recebida",
        )
        assert data.status == StatusOrdemServico.RECEBIDA

    def test_ordem_servico_update_status_only(self):
        data = OrdemServicoUpdate(status="em_execucao")
        assert data.status == StatusOrdemServico.EM_EXECUCAO

    def test_ordem_servico_invalid_status(self):
        with pytest.raises(ValueError):
            OrdemServicoUpdate(status="invalid_status")

    def test_data_abertura_optional(self):
        data = OrdemServicoInput(
            cliente_id="cli",
            vehicle_id=456,  # 🔁 agora é int
            servico_ids=["1"],
            status="recebida"
        )
        assert data.vehicle_id == 456