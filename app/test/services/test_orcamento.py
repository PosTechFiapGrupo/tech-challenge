import pytest
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from app.application.services.orcamento import OrcamentoService
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.servico import ServicoEntity
from app.domain.entities.inventory_item_entity import InventoryItem
from app.domain.entities.ordem_servico_servico import OrdemServicoServicoEntity
from app.domain.entities.ordem_servico_inventory_item import OrdemServicoInventoryItemEntity
from app.domain.entities.status_ordem_servico import StatusOrdemServico


@pytest.fixture
def mock_ordem_servico_repository():
    return Mock()


@pytest.fixture
def mock_servico_repository():
    return Mock()


@pytest.fixture
def mock_inventory_repository():
    return Mock()


@pytest.fixture
def mock_os_servico_repository():
    return Mock()


@pytest.fixture
def mock_os_inventory_repository():
    return Mock()


@pytest.fixture
def orcamento_service(
    mock_ordem_servico_repository,
    mock_servico_repository,
    mock_inventory_repository,
    mock_os_servico_repository,
    mock_os_inventory_repository,
):
    return OrcamentoService(
        ordem_servico_repository=mock_ordem_servico_repository,
        servico_repository=mock_servico_repository,
        inventory_repository=mock_inventory_repository,
        os_servico_repository=mock_os_servico_repository,
        os_inventory_repository=mock_os_inventory_repository,
    )


@pytest.fixture
def sample_ordem_servico():
    return OrdemServicoEntity(
        uid="os-123",
        cliente_id="cliente-456",
        vehicle_id=789,
        servico_ids=["servico-1", "servico-2"],
        status=StatusOrdemServico.RECEBIDA,
    )


@pytest.fixture
def sample_servico():
    return ServicoEntity(
        uid="servico-1",
        descricao="Troca de óleo",
        preco=50.00
    )


@pytest.fixture
def sample_inventory_item():
    return InventoryItem(
        id=1,
        name="Óleo 5W30",
        description="Óleo sintético para motor",
        quantity=10,
        minimum_stock=2,
        unit_price=25.50
    )


@pytest.fixture
def sample_os_servico():
    return OrdemServicoServicoEntity(
        id=1,
        ordem_servico_id="os-123",
        servico_id="servico-1",
        valor_servico=Decimal("50.00"),
        observacoes="Serviço padrão"
    )


@pytest.fixture
def sample_os_inventory_item():
    return OrdemServicoInventoryItemEntity(
        id=1,
        ordem_servico_id="os-123",
        inventory_item_id=1,
        quantidade=2,
        valor_unitario=Decimal("25.50")
    )


class TestOrcamentoService:

    @pytest.mark.asyncio
    async def test_gerar_orcamento_com_servicos_e_itens(
        self,
        orcamento_service,
        mock_ordem_servico_repository,
        mock_servico_repository,
        mock_inventory_repository,
        mock_os_servico_repository,
        mock_os_inventory_repository,
        sample_ordem_servico,
        sample_servico,
        sample_inventory_item,
        sample_os_servico,
        sample_os_inventory_item,
    ):
        # Arrange
        ordem_servico_id = "os-123"
        
        mock_ordem_servico_repository.get_by_id = AsyncMock(return_value=sample_ordem_servico)
        mock_os_servico_repository.listar_servicos_por_os = AsyncMock(return_value=[sample_os_servico])
        mock_os_inventory_repository.listar_itens_por_os = AsyncMock(return_value=[sample_os_inventory_item])
        mock_servico_repository.get_by_id = AsyncMock(return_value=sample_servico)
        mock_inventory_repository.get_by_id = AsyncMock(return_value=sample_inventory_item)

        # Act
        resultado = await orcamento_service.gerar_orcamento(ordem_servico_id)

        # Assert
        assert resultado is not None
        assert resultado.ordem_servico.id == "os-123"
        assert len(resultado.servicos) == 1
        assert len(resultado.inventory_items) == 1
        assert resultado.total_servicos == Decimal("50.00")
        assert resultado.total_items == Decimal("51.00")  # 2 * 25.50
        assert resultado.total_geral == Decimal("101.00")

        # Verify repository calls
        mock_ordem_servico_repository.get_by_id.assert_called_once_with(ordem_servico_id)
        mock_os_servico_repository.listar_servicos_por_os.assert_called_once_with(ordem_servico_id)
        mock_os_inventory_repository.listar_itens_por_os.assert_called_once_with(ordem_servico_id)

    @pytest.mark.asyncio
    async def test_gerar_orcamento_apenas_servicos(
        self,
        orcamento_service,
        mock_ordem_servico_repository,
        mock_servico_repository,
        mock_inventory_repository,
        mock_os_servico_repository,
        mock_os_inventory_repository,
        sample_ordem_servico,
        sample_servico,
        sample_os_servico,
    ):
        # Arrange
        ordem_servico_id = "os-123"
        
        mock_ordem_servico_repository.get_by_id = AsyncMock(return_value=sample_ordem_servico)
        mock_os_servico_repository.listar_servicos_por_os = AsyncMock(return_value=[sample_os_servico])
        mock_os_inventory_repository.listar_itens_por_os = AsyncMock(return_value=[])
        mock_servico_repository.get_by_id = AsyncMock(return_value=sample_servico)

        # Act
        resultado = await orcamento_service.gerar_orcamento(ordem_servico_id)

        # Assert
        assert resultado is not None
        assert len(resultado.servicos) == 1
        assert len(resultado.inventory_items) == 0
        assert resultado.total_servicos == Decimal("50.00")
        assert resultado.total_items == Decimal("0.00")
        assert resultado.total_geral == Decimal("50.00")

    @pytest.mark.asyncio
    async def test_gerar_orcamento_ordem_servico_nao_encontrada(
        self,
        orcamento_service,
        mock_ordem_servico_repository,
    ):
        # Arrange
        ordem_servico_id = "os-inexistente"
        mock_ordem_servico_repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(ValueError, match="Ordem de serviço não encontrada"):
            await orcamento_service.gerar_orcamento(ordem_servico_id)

    @pytest.mark.asyncio
    async def test_gerar_orcamento_sem_servicos_e_itens(
        self,
        orcamento_service,
        mock_ordem_servico_repository,
        mock_os_servico_repository,
        mock_os_inventory_repository,
        sample_ordem_servico,
    ):
        # Arrange
        ordem_servico_id = "os-123"
        
        mock_ordem_servico_repository.get_by_id = AsyncMock(return_value=sample_ordem_servico)
        mock_os_servico_repository.listar_servicos_por_os = AsyncMock(return_value=[])
        mock_os_inventory_repository.listar_itens_por_os = AsyncMock(return_value=[])

        # Act
        resultado = await orcamento_service.gerar_orcamento(ordem_servico_id)

        # Assert
        assert resultado is not None
        assert len(resultado.servicos) == 0
        assert len(resultado.inventory_items) == 0
        assert resultado.total_servicos == Decimal("0.00")
        assert resultado.total_items == Decimal("0.00")
        assert resultado.total_geral == Decimal("0.00")

    @pytest.mark.asyncio
    async def test_gerar_orcamento_calculo_valores_multiplos_itens(
        self,
        orcamento_service,
        mock_ordem_servico_repository,
        mock_servico_repository,
        mock_inventory_repository,
        mock_os_servico_repository,
        mock_os_inventory_repository,
        sample_ordem_servico,
        sample_servico,
        sample_inventory_item,
    ):
        # Arrange
        ordem_servico_id = "os-123"
        
        # Múltiplos serviços
        os_servico_1 = OrdemServicoServicoEntity(
            id=1,
            ordem_servico_id="os-123",
            servico_id="servico-1",
            valor_servico=Decimal("50.00"),
            observacoes=None
        )
        os_servico_2 = OrdemServicoServicoEntity(
            id=2,
            ordem_servico_id="os-123",
            servico_id="servico-2",
            valor_servico=Decimal("75.00"),
            observacoes=None
        )
        
        # Múltiplos itens de inventário
        os_item_1 = OrdemServicoInventoryItemEntity(
            id=1,
            ordem_servico_id="os-123",
            inventory_item_id=1,
            quantidade=2,
            valor_unitario=Decimal("25.50")
        )
        os_item_2 = OrdemServicoInventoryItemEntity(
            id=2,
            ordem_servico_id="os-123",
            inventory_item_id=2,
            quantidade=3,
            valor_unitario=Decimal("10.00")
        )
        
        mock_ordem_servico_repository.get_by_id = AsyncMock(return_value=sample_ordem_servico)
        mock_os_servico_repository.listar_servicos_por_os = AsyncMock(return_value=[os_servico_1, os_servico_2])
        mock_os_inventory_repository.listar_itens_por_os = AsyncMock(return_value=[os_item_1, os_item_2])
        mock_servico_repository.get_by_id = AsyncMock(return_value=sample_servico)
        mock_inventory_repository.get_by_id = AsyncMock(return_value=sample_inventory_item)

        # Act
        resultado = await orcamento_service.gerar_orcamento(ordem_servico_id)

        # Assert
        assert resultado.total_servicos == Decimal("125.00")  # 50 + 75
        assert resultado.total_items == Decimal("81.00")  # (2 * 25.50) + (3 * 10.00)
        assert resultado.total_geral == Decimal("206.00")  # 125 + 81
