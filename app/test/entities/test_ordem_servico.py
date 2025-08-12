import pytest
from datetime import datetime
import uuid
from app.domain.entities.ordem_servico import OrdemServicoEntity, OrdemServicoEntityFactory
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class TestOrdemServicoEntity:

    def test_create_ordem_servico_minimal(self):
        os = OrdemServicoEntity(
            uid="os-1",
            cliente_id="cli-1",
            vehicle_id=1,
            servico_ids=["s1", "s2"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert os.id == "os-1"
        assert os.status == StatusOrdemServico.RECEBIDA
        assert isinstance(os.data_abertura, datetime)
        assert os.data_fechamento is None

    def test_create_ordem_servico_full_fields(self):
        abertura = datetime(2025, 1, 1)
        fechamento = datetime(2025, 1, 2)
        os = OrdemServicoEntity(
            uid="os-2",
            cliente_id="cli-2",
            vehicle_id=2,
            servico_ids=["s3"],
            mecanico_id="mec-1",
            atendente_id="atd-1",
            orcamento_id="orc-1",
            status=StatusOrdemServico.FINALIZADA,
            data_abertura=abertura,
            data_fechamento=fechamento,
        )
        assert os.mecanico_id == "mec-1"
        assert os.atendente_id == "atd-1"
        assert os.orcamento_id == "orc-1"
        assert os.data_abertura == abertura
        assert os.data_fechamento == fechamento
        assert os.status == StatusOrdemServico.FINALIZADA

    def test_iniciar_execucao_valido(self):
        os = OrdemServicoEntity(
            uid="os-3",
            cliente_id="cli-3",
            vehicle_id=3,
            servico_ids=["s4"],
            status=StatusOrdemServico.RECEBIDA,
        )
        os.iniciar_execucao()
        assert os.status == StatusOrdemServico.EM_EXECUCAO

    def test_iniciar_execucao_invalido(self):
        os = OrdemServicoEntity(
            uid="os-4",
            cliente_id="cli-4",
            vehicle_id=4,
            servico_ids=["s5"],
            status=StatusOrdemServico.EM_EXECUCAO,
        )
        with pytest.raises(ValueError, match="Não é possível iniciar execução"):
            os.iniciar_execucao()

    def test_finalizar_valido(self):
        os = OrdemServicoEntity(
            uid="os-5",
            cliente_id="cli-5",
            vehicle_id=5,
            servico_ids=["s6"],
            status=StatusOrdemServico.EM_EXECUCAO,
        )
        os.finalizar()
        assert os.status == StatusOrdemServico.FINALIZADA
        assert isinstance(os.data_fechamento, datetime)

    def test_finalizar_invalido(self):
        os = OrdemServicoEntity(
            uid="os-6",
            cliente_id="cli-6",
            vehicle_id=6,
            servico_ids=["s7"],
            status=StatusOrdemServico.RECEBIDA,
        )
        with pytest.raises(ValueError, match="Não é possível finalizar"):
            os.finalizar()

    def test_cancelar_valido(self):
        os = OrdemServicoEntity(
            uid="os-7",
            cliente_id="cli-7",
            vehicle_id=7,
            servico_ids=["s8"],
            status=StatusOrdemServico.RECEBIDA,
        )
        os.cancelar()
        assert os.status == StatusOrdemServico.CANCELADA

    def test_cancelar_invalido(self):
        os = OrdemServicoEntity(
            uid="os-8",
            cliente_id="cli-8",
            vehicle_id=8,
            servico_ids=["s9"],
            status=StatusOrdemServico.FINALIZADA,
        )
        with pytest.raises(ValueError, match="Não é possível cancelar"):
            os.cancelar()


class TestOrdemServicoEntityFactory:

    def test_create_ordem_servico_with_id(self):
        os = OrdemServicoEntityFactory.create(
            id="os-9",
            cliente_id="cli-9",
            vehicle_id=9,
            servico_ids=["s10", "s11"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert os.id == "os-9"
        assert os.status == StatusOrdemServico.RECEBIDA

    def test_create_ordem_servico_without_id_generates_uuid(self):
        os = OrdemServicoEntityFactory.create(
            id=None,
            cliente_id="cli-10",
            vehicle_id=10,
            servico_ids=["s12"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert isinstance(os.id, str)
        assert uuid.UUID(os.id)  # Valida que é um UUID válido
