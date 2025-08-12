import pytest
from unittest.mock import AsyncMock, Mock
from app.application.services.cliente import ClienteService
from app.domain.entities.cliente import ClienteEntity


class TestClienteService:

    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()

    @pytest.fixture
    def mock_created_event(self):
        return Mock()

    @pytest.fixture
    def mock_updated_event(self):
        return Mock()

    @pytest.fixture
    def mock_deleted_event(self):
        return Mock()

    @pytest.fixture
    def cliente_service(
        self,
        mock_repository,
        mock_created_event,
        mock_updated_event,
        mock_deleted_event,
    ):
        return ClienteService(
            mock_repository, mock_created_event, mock_updated_event, mock_deleted_event
        )

    @pytest.fixture
    def sample_cliente(self):
        return ClienteEntity(
            "1", "João Silva", "11999999999", "joao@email.com", "12345678901"
        )

    # --- Testes existentes ---
    @pytest.mark.asyncio
    async def test_get_all_clientes(
        self, cliente_service, mock_repository, sample_cliente
    ):
        mock_repository.get_all.return_value = [sample_cliente]

        result = await cliente_service.get_all_clientes()

        assert len(result) == 1
        assert result[0].nome == "João Silva"
        mock_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cliente_by_id(
        self, cliente_service, mock_repository, sample_cliente
    ):
        mock_repository.get_by_id.return_value = sample_cliente

        result = await cliente_service.get_cliente_by_id("1")

        assert result.nome == "João Silva"
        mock_repository.get_by_id.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_create_cliente(
        self, cliente_service, mock_repository, mock_created_event, sample_cliente
    ):
        mock_repository.add.return_value = sample_cliente

        result = await cliente_service.create_cliente(sample_cliente)

        assert result.nome == "João Silva"
        mock_repository.add.assert_called_once_with(sample_cliente)
        mock_created_event.send.assert_called_once_with(sample_cliente)

    @pytest.mark.asyncio
    async def test_create_cliente_with_invalid_nome(self, cliente_service):
        cliente = ClienteEntity("1", "", "11999999999", "joao@email.com", "12345678901")

        with pytest.raises(ValueError):
            await cliente_service.create_cliente(cliente)

    # --- Novos testes ---
    @pytest.mark.asyncio
    async def test_get_cliente_by_cpf(self, cliente_service, mock_repository, sample_cliente):
        mock_repository.get_by_cpf.return_value = sample_cliente

        result = await cliente_service.get_cliente_by_cpf("12345678901")

        assert result == sample_cliente
        mock_repository.get_by_cpf.assert_called_once_with("12345678901")

    @pytest.mark.asyncio
    async def test_update_cliente(self, cliente_service, mock_repository, mock_updated_event, sample_cliente):
        mock_repository.update.return_value = sample_cliente

        result = await cliente_service.update_cliente(sample_cliente)

        assert result == sample_cliente
        mock_repository.update.assert_called_once_with(sample_cliente)
        mock_updated_event.send.assert_called_once_with(sample_cliente)

    @pytest.mark.asyncio
    async def test_delete_cliente_success(self, cliente_service, mock_repository, mock_deleted_event):
        mock_repository.delete.return_value = True

        result = await cliente_service.delete_cliente("1")

        assert result is True
        mock_repository.delete.assert_called_once_with("1")
        mock_deleted_event.send.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_delete_cliente_not_found(self, cliente_service, mock_repository, mock_deleted_event):
        mock_repository.delete.return_value = False

        result = await cliente_service.delete_cliente("1")

        assert result is False
        mock_repository.delete.assert_called_once_with("1")
        mock_deleted_event.send.assert_not_called()