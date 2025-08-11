import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.infrastructure.fast_api import create_app
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.auth_dependencies import get_current_user


@pytest.fixture(scope="function")
def app():
    app = create_app()
    yield app


@pytest_asyncio.fixture(scope="function")
async def async_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_user():
    return UserEntity(
        uid="1",
        nome="Admin Test",
        email="admin@test.com",
        hashed_password="fakehashedpassword",
        funcao=UserFuncao.ADMIN,
    )


@pytest.fixture(scope="function")
def mock_password_service():
    mock = AsyncMock()
    mock.verify_password.return_value = True
    mock.hash_password.return_value = "fakehashedpassword"
    return mock


@pytest.fixture(scope="function")
def mock_user_service(mock_user, mock_password_service):
    mock = AsyncMock()

    async def get_user_by_email(email):
        return mock_user if email == "admin@test.com" else None

    async def get_user_by_id(user_id):
        return mock_user if user_id == "1" else None

    async def fake_create_user(user_entity, plain_password):
        return user_entity

    mock.get_user_by_email.side_effect = get_user_by_email
    mock.get_user_by_id.side_effect = get_user_by_id
    mock.create_user.side_effect = fake_create_user

    mock.password_service = mock_password_service

    return mock


@pytest.fixture(scope="function")
def mock_ordem_servico_service():
    mock = AsyncMock()

    # Mocks dos métodos
    mock.criar_ordem_servico = AsyncMock()
    mock.listar_ordens_servico = AsyncMock()
    mock.buscar_ordem_servico_por_id = AsyncMock()
    mock.atualizar_ordem_servico = AsyncMock()
    mock.iniciar_execucao = AsyncMock()
    mock.finalizar = AsyncMock()
    mock.cancelar = AsyncMock()

    mock.cliente_validator = AsyncMock()
    mock.cliente_validator.validate_exists = AsyncMock()

    mock.vehicle_validator = AsyncMock()
    mock.vehicle_validator.validate_exists = AsyncMock()

    mock.servico_validator = AsyncMock()
    mock.servico_validator.validate_exists = AsyncMock()

    mock.validator = AsyncMock()
    mock.validator.validate_status_transition = AsyncMock()

    return mock


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def override_services(app, mock_ordem_servico_service, mock_user_service, mock_password_service):
    app.container.ordem_servico_service.override(mock_ordem_servico_service)
    app.container.user_service.override(mock_user_service)
    app.container.password_service.override(mock_password_service)

    async def fake_get_current_user():
        return await mock_user_service.get_user_by_email("admin@test.com")

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.container.ordem_servico_service.reset_override()
    app.container.user_service.reset_override()
    app.container.password_service.reset_override()
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestOrdemServicoAPI:

    async def test_criar_ordem_servico_sucesso(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
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

        response = await async_client.post("/ordens-servico/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["cliente_id"] == "cliente-123"
        assert data["status"] == "recebida"

    async def test_listar_ordens_servico(self, async_client, override_services, mock_ordem_servico_service):
        from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput
        from datetime import datetime

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

        response = await async_client.get("/ordens-servico/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]["id"] == "os-1"
        assert response.json()[0]["status"] == "recebida"

    async def test_buscar_ordem_servico_por_id_sucesso(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
    ):
        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = sample_ordem_servico

        response = await async_client.get("/ordens-servico/os-1")

        assert response.status_code == 200
        assert response.json()["id"] == "os-1"

    async def test_buscar_ordem_servico_por_id_nao_encontrada(
        self, async_client, override_services, mock_ordem_servico_service
    ):
        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = None

        response = await async_client.get("/ordens-servico/os-inexistente")

        assert response.status_code == 404

    async def test_atualizar_ordem_servico(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
    ):
        mock_ordem_servico_service.buscar_ordem_servico_por_id.return_value = sample_ordem_servico
        sample_ordem_servico.status = StatusOrdemServico.EM_DIAGNOSTICO
        mock_ordem_servico_service.atualizar_ordem_servico.return_value = sample_ordem_servico

        payload = {"status": "em_diagnostico"}

        response = await async_client.put("/ordens-servico/os-1", json=payload)

        assert response.status_code == 200
        assert response.json()["status"] == "em_diagnostico"

    async def test_atualizar_ordem_servico_nao_encontrada(
        self, async_client, override_services, mock_ordem_servico_service
    ):
        mock_ordem_servico_service.atualizar_ordem_servico.side_effect = ValueError(
            "Ordem de serviço não encontrada"
        )

        payload = {"status": "em_execucao"}

        response = await async_client.put("/ordens-servico/os-nao-existe", json=payload)

        assert response.status_code == 400  # ou 404 conforme implementação

    async def test_iniciar_execucao_ordem_servico(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
    ):
        sample_ordem_servico.status = StatusOrdemServico.EM_EXECUCAO
        mock_ordem_servico_service.iniciar_execucao.return_value = sample_ordem_servico

        response = await async_client.put("/ordens-servico/os-1/iniciar-execucao")

        assert response.status_code == 200
        assert response.json()["status"] == "em_execucao"

    async def test_finalizar_ordem_servico(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
    ):
        sample_ordem_servico.status = StatusOrdemServico.FINALIZADA
        sample_ordem_servico.data_fechamento = datetime.now(timezone.utc)
        mock_ordem_servico_service.finalizar.return_value = sample_ordem_servico

        response = await async_client.put("/ordens-servico/os-1/finalizar")

        assert response.status_code == 200
        assert response.json()["status"] == "finalizada"

    async def test_cancelar_ordem_servico(
        self, async_client, override_services, mock_ordem_servico_service, sample_ordem_servico
    ):
        sample_ordem_servico.status = StatusOrdemServico.CANCELADA
        sample_ordem_servico.data_fechamento = datetime.now(timezone.utc)
        mock_ordem_servico_service.cancelar.return_value = sample_ordem_servico

        response = await async_client.put("/ordens-servico/os-1/cancelar")

        assert response.status_code == 200
        assert response.json()["status"] == "cancelada"

    async def test_transicao_status_invalida(
        self, async_client, override_services, mock_ordem_servico_service
    ):
        mock_ordem_servico_service.iniciar_execucao.side_effect = ValueError(
            "Transição inválida de status: RECEBIDA → EM_EXECUCAO"
        )

        response = await async_client.put("/ordens-servico/os-1/iniciar-execucao")

        assert response.status_code == 400
        assert "Transição inválida" in response.json()["detail"]
