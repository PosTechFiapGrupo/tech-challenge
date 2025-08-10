import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.infrastructure.fast_api import create_app
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from datetime import datetime, timezone


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_ordem_servico_service():
    service = AsyncMock()
    service.criar_ordem_servico = AsyncMock()
    service.listar_ordens_servico = AsyncMock()
    service.buscar_ordem_servico_por_id = AsyncMock()
    service.atualizar_ordem_servico = AsyncMock()
    service.iniciar_execucao = AsyncMock()
    service.finalizar = AsyncMock()
    service.cancelar = AsyncMock()

    service.cliente_validator = AsyncMock()
    service.cliente_validator.validate_exists = AsyncMock()

    service.vehicle_validator = AsyncMock()
    service.vehicle_validator.validate_exists = AsyncMock()

    service.servico_validator = AsyncMock()
    service.servico_validator.validate_exists = AsyncMock()

    service.validator = AsyncMock()
    service.validator.validate_status_transition = AsyncMock()

    return service


@pytest.fixture
def sample_ordem_servico():
    return OrdemServicoEntity(
        uid="os-1",
        cliente_id="cliente-123",
        vehicle_id=456,
        servico_ids=["serv-1", "serv-2"],
        status=StatusOrdemServico.RECEBIDA,
        data_abertura=datetime.now(timezone.utc),
        data_fechamento=None,
        atendente_id="atend-1",
        mecanico_id="mec-1",
        orcamento_id="orc-1",
    )


class TestOrdemServicoAPI:

    def test_criar_ordem_servico_sucesso(
            self, client, mock_ordem_servico_service, sample_ordem_servico
    ):
        payload = {
            "cliente_id": "cliente-123",
            "vehicle_id": 456,
            "servico_ids": ["serv-1", "serv-2"],
            "status": "recebida",
        }

        mock_ordem_servico_service.criar_ordem_servico.return_value = sample_ordem_servico

        mock_ordem_servico_service.cliente_validator.validate_exists.return_value = None
        mock_ordem_servico_service.vehicle_validator.validate_exists.return_value = None
        mock_ordem_servico_service.servico_validator.validate_exists.return_value = None

        with client.app.container.ordem_servico_service.override(mock_ordem_servico_service):
            response = client.post("/ordens-servico/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["cliente_id"] == "cliente-123"
        assert data["status"] == "recebida"

    def test_listar_ordens_servico(self, client, mock_ordem_servico_service):
        mock_ordem_servico_service.listar_ordens_servico.return_value = [
            OrdemServicoOutput(
                id="os-1",
                cliente_id="cli-1",
                vehicle_id=456,
                servico_ids=["s1", "s2"],
                status=StatusOrdemServico.RECEBIDA,
                data_abertura=datetime.fromisoformat("2025-08-05T00:00:00+00:00"),
            )
        ]

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.get("/ordens-servico/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]["id"] == "os-1"
        assert response.json()[0]["status"] == "recebida"

    def test_buscar_ordem_servico_por_id_sucesso(
        self, client, mock_ordem_servico_service, sample_ordem_servico
    ):
        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = (
            sample_ordem_servico
        )

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.get("/ordens-servico/os-1")

        assert response.status_code == 200
        assert response.json()["id"] == "os-1"

    def test_buscar_ordem_servico_por_id_nao_encontrada(
        self, client, mock_ordem_servico_service
    ):
        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = None

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.get("/ordens-servico/os-inexistente")

        assert response.status_code == 404

    def test_atualizar_ordem_servico(
        self, client, mock_ordem_servico_service, sample_ordem_servico
    ):
        from app.infrastructure.schemas.ordem_servico import OrdemServicoUpdate

        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = (
            sample_ordem_servico
        )
        sample_ordem_servico.status = StatusOrdemServico.EM_DIAGNOSTICO
        mock_ordem_servico_service.atualizar_ordem_servico.return_value = (
            sample_ordem_servico
        )

        payload = {"status": "em_diagnostico"}

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.put("/ordens-servico/os-1", json=payload)

        assert response.status_code == 200
        assert response.json()["status"] == "em_diagnostico"

    def test_atualizar_ordem_servico_nao_encontrada(
        self, client, mock_ordem_servico_service
    ):
        mock_ordem_servico_service.atualizar_ordem_servico.side_effect = ValueError(
            "Ordem de serviço não encontrada"
        )

        payload = {"status": "em_execucao"}

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.put("/ordens-servico/os-nao-existe", json=payload)

        assert response.status_code == 400  # ou 404 se você quiser mudar no endpoint

    def test_iniciar_execucao_ordem_servico(
        self, client, mock_ordem_servico_service, sample_ordem_servico
    ):
        sample_ordem_servico.status = StatusOrdemServico.EM_EXECUCAO
        mock_ordem_servico_service.iniciar_execucao.return_value = sample_ordem_servico

        with client.app.container.ordem_servico_service.override(
            mock_ordem_servico_service
        ):
            response = client.put("/ordens-servico/os-1/iniciar-execucao")

        assert response.status_code == 200
        assert response.json()["status"] == "em_execucao"

    def test_finalizar_ordem_servico(self, client, mock_ordem_servico_service, sample_ordem_servico):
        from datetime import datetime, timezone

        sample_ordem_servico.status = StatusOrdemServico.FINALIZADA
        sample_ordem_servico.data_fechamento = datetime.now(timezone.utc)

        # 👇 Isso aqui é o correto — sem sobrescrever o método
        mock_ordem_servico_service.finalizar.return_value = sample_ordem_servico

        with client.app.container.ordem_servico_service.override(mock_ordem_servico_service):
            response = client.put("/ordens-servico/os-1/finalizar")

        assert response.status_code == 200
        assert response.json()["status"] == "finalizada"

    def test_cancelar_ordem_servico(self, client, mock_ordem_servico_service, sample_ordem_servico):
        sample_ordem_servico.status = StatusOrdemServico.CANCELADA
        sample_ordem_servico.data_fechamento = datetime.now(timezone.utc)

        mock_ordem_servico_service.cancelar.return_value = sample_ordem_servico

        with client.app.container.ordem_servico_service.override(mock_ordem_servico_service):
            response = client.put("/ordens-servico/os-1/cancelar")

        assert response.status_code == 200
        assert response.json()["status"] == "cancelada"

    def test_transicao_status_invalida(self, client, mock_ordem_servico_service):
        mock_ordem_servico_service.iniciar_execucao.side_effect = ValueError(
            "Transição inválida de status: RECEBIDA → EM_EXECUCAO"
        )

        with client.app.container.ordem_servico_service.override(mock_ordem_servico_service):
            response = client.put("/ordens-servico/os-1/iniciar-execucao")

        assert response.status_code == 400
        assert "Transição inválida" in response.json()["detail"]
