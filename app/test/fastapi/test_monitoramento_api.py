import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from datetime import timedelta
from fastapi import status
from app.infrastructure.fast_api import create_app
from app.infrastructure.schemas.monitoramento_schema import TempoMedioServicosOut
from app.infrastructure.auth_dependencies import get_current_user
from app.domain.entities.user import UserEntity, UserFuncao

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
def mock_monitoramento_service():
    mock = AsyncMock()
    return mock

@pytest.fixture(scope="function")
def override_services(app, mock_monitoramento_service, mock_user):
    app.dependency_overrides = {}

    # Mock para o método do serviço
    async def fake_tempo_medio():
        return await mock_monitoramento_service.obter_tempo_medio()

    # Mock do usuário autenticado (para evitar 401)
    async def fake_get_current_user():
        return mock_user

    # Override da dependência de autenticação e do serviço
    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield

    app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestMonitoramentoAPI:

    async def test_tempo_medio_servicos_success(self, async_client, mock_monitoramento_service, override_services):
        # Mocka um timedelta de 1 dia, 2 horas, 30 minutos
        mock_monitoramento_service.obter_tempo_medio.return_value = timedelta(days=1, hours=2, minutes=30)

        # Patch do método obter_tempo_medio do serviço para usar o mock
        with patch("app.application.services.monitoramento_service.MonitoramentoService.obter_tempo_medio", 
                   mock_monitoramento_service.obter_tempo_medio):
            response = await async_client.get("/monitoramento/tempo-medio-servicos")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["dias"] == 1
        assert data["horas"] == 2
        assert data["minutos"] == 30

    async def test_tempo_medio_servicos_none(self, async_client, mock_monitoramento_service, override_services):
        mock_monitoramento_service.obter_tempo_medio.return_value = None

        from app.application.services.monitoramento_service import MonitoramentoService
        from unittest.mock import patch

        with patch.object(MonitoramentoService, "obter_tempo_medio", mock_monitoramento_service.obter_tempo_medio):
            response = await async_client.get("/monitoramento/tempo-medio-servicos")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Nenhum serviço finalizado"