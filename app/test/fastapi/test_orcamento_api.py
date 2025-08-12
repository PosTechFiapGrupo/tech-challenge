import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from decimal import Decimal
from fastapi import status
from app.infrastructure.fast_api import create_app
from app.domain.entities.user import UserEntity, UserFuncao
from app.infrastructure.auth_dependencies import get_current_user
from app.infrastructure.schemas.orcamento import OrcamentoOutput
from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput
from app.infrastructure.schemas.servico import ServicoOutput
from app.infrastructure.schemas.inventory_item_schema import InventoryItemOut
from app.application.services.orcamento import OrcamentoService
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from datetime import datetime

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
def mock_orcamento_service():
    mock = AsyncMock()

    # Mock de um orçamento de exemplo
    ordem_servico = OrdemServicoOutput(
        id="os123",
        cliente_id="cliente1",
        vehicle_id=1,
        servico_ids=["s1"],
        status=StatusOrdemServico.RECEBIDA,
        data_abertura=datetime.utcnow(),
        data_fechamento=None,
        atendente_id="1",
        mecanico_id=None,
        orcamento_id=None,
    )

    servico_orcamento = {
        "servico": ServicoOutput(id="s1", descricao="Troca de óleo", preco=100.0),
        "valor_na_os": Decimal("90.0"),
        "observacoes": "Desconto aplicado",
    }

    inventory_item_orcamento = {
        "item": InventoryItemOut(
            id=1,
            name="Óleo 5W30",
            description="Lubrificante para motor",
            quantity=10,
            minimum_stock=3,
            unit_price=50.0,
        ),
        "quantidade": 2,
        "valor_unitario_na_os": Decimal("50.0"),
        "valor_total": Decimal("100.0"),
    }

    orcamento = OrcamentoOutput(
        ordem_servico=ordem_servico,
        servicos=[servico_orcamento],
        inventory_items=[inventory_item_orcamento],
        total_servicos=Decimal("90.0"),
        total_items=Decimal("100.0"),
        total_geral=Decimal("190.0"),
    )

    mock.gerar_orcamento.return_value = orcamento
    return mock

@pytest.fixture(scope="function")
def override_auth(app, mock_user):
    async def fake_get_current_user():
        return mock_user
    app.dependency_overrides[get_current_user] = fake_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def override_services(app, mock_orcamento_service):
    app.container.orcamento_service.override(mock_orcamento_service)
    yield
    app.container.orcamento_service.reset_override()

@pytest.fixture(scope="function")
def combined_overrides(app, override_services, override_auth):
    yield

@pytest.mark.asyncio
class TestOrcamentoAPI:

    async def test_gerar_orcamento_success(self, async_client, combined_overrides):
        response = await async_client.get("/ordens-servico/os123/orcamento")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ordem_servico"]["id"] == "os123"
        assert data["total_geral"] == "190.0"
        assert len(data["servicos"]) == 1
        assert len(data["inventory_items"]) == 1

    async def test_gerar_orcamento_not_found(self, async_client, combined_overrides, mock_orcamento_service):
        mock_orcamento_service.gerar_orcamento.side_effect = ValueError("Orçamento não encontrado")

        response = await async_client.get("/ordens-servico/nao-existe/orcamento")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Orçamento não encontrado"
