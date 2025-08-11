import pytest
from unittest.mock import AsyncMock, Mock
from app.application.services.servico import ServicoService
from app.domain.entities.servico import ServicoEntity


class TestServicoService:

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
    def servico_service(
        self,
        mock_repository,
        mock_created_event,
        mock_updated_event,
        mock_deleted_event,
    ):
        return ServicoService(
            mock_repository, mock_created_event, mock_updated_event, mock_deleted_event
        )

    @pytest.fixture
    def sample_servico(self):
        return ServicoEntity("1", "Consultoria em TI", 150.00)

    @pytest.mark.asyncio
    async def test_get_all_servicos(
        self, servico_service, mock_repository, sample_servico
    ):
        mock_repository.get_all.return_value = [sample_servico]

        result = await servico_service.get_all_servicos()

        assert len(result) == 1
        assert result[0].descricao == "Consultoria em TI"
        mock_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_servico_by_id(
        self, servico_service, mock_repository, sample_servico
    ):
        mock_repository.get_by_id.return_value = sample_servico

        result = await servico_service.get_servico_by_id("1")

        assert result.descricao == "Consultoria em TI"
        mock_repository.get_by_id.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_create_servico(
        self, servico_service, mock_repository, mock_created_event, sample_servico
    ):
        mock_repository.add.return_value = sample_servico

        result = await servico_service.create_servico(sample_servico)

        assert result.descricao == "Consultoria em TI"
        mock_repository.add.assert_called_once_with(sample_servico)
        mock_created_event.send.assert_called_once_with(sample_servico)

    @pytest.mark.asyncio
    async def test_create_servico_with_invalid_descricao(self, servico_service):
        from app.domain.exceptions import InvalidDescription

        with pytest.raises(InvalidDescription):
            servico = ServicoEntity("1", "", 150.00)
