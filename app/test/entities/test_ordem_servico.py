import pytest
from app.domain.entities.ordem_servico import (
    OrdemServicoEntity,
    OrdemServicoEntityFactory,
)
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from datetime import datetime


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
        assert os.data_abertura is not None

    def test_ordem_servico_default_data_abertura(self):
        os = OrdemServicoEntity(
            uid="os-2",
            cliente_id="cli-2",
            vehicle_id=2,
            servico_ids=["s3"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert isinstance(os.data_abertura, datetime)

    def test_ordem_servico_status_enum(self):
        os = OrdemServicoEntity(
            uid="os-3",
            cliente_id="cli-3",
            vehicle_id=3,
            servico_ids=["s4"],
            status=StatusOrdemServico.EM_DIAGNOSTICO,
        )
        assert os.status == StatusOrdemServico.EM_DIAGNOSTICO


class TestOrdemServicoEntityFactory:

    def test_create_ordem_servico_with_id(self):
        os = OrdemServicoEntityFactory.create(
            id="os-4",
            cliente_id="cli-4",
            vehicle_id=4,
            servico_ids=["s5", "s6"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert os.id == "os-4"
        assert os.status == StatusOrdemServico.RECEBIDA

    def test_create_ordem_servico_without_id_generates_uuid(self):
        os = OrdemServicoEntityFactory.create(
            id=None,
            cliente_id="cli-5",
            vehicle_id=5,
            servico_ids=["s7"],
            status=StatusOrdemServico.RECEBIDA,
        )
        assert os.id is not None
        assert len(os.id) == 36  # UUID length
