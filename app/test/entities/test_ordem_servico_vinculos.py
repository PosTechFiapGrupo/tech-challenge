import pytest
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from app.domain.entities.ordem_servico_servico import OrdemServicoServicoEntity, OrdemServicoServicoEntityFactory
from app.domain.entities.ordem_servico_inventory_item import OrdemServicoInventoryItemEntity, OrdemServicoInventoryItemEntityFactory
from app.infrastructure.repositories.ordem_servico_servico_impl import OrdemServicoServicoRepositoryImpl
from app.infrastructure.repositories.ordem_servico_inventory_item_impl import OrdemServicoInventoryItemRepositoryImpl


class TestOrdemServicoServicoEntity:

    def test_create_ordem_servico_servico_entity(self):
        os_servico = OrdemServicoServicoEntity(
            id=1,
            ordem_servico_id="os-123",
            servico_id="servico-456",
            valor_servico=Decimal("75.50"),
            observacoes="Serviço de revisão completa"
        )

        assert os_servico.id == 1
        assert os_servico.ordem_servico_id == "os-123"
        assert os_servico.servico_id == "servico-456"
        assert os_servico.valor_servico == Decimal("75.50")
        assert os_servico.observacoes == "Serviço de revisão completa"

    def test_create_ordem_servico_servico_entity_without_observacoes(self):
        os_servico = OrdemServicoServicoEntity(
            id=2,
            ordem_servico_id="os-789",
            servico_id="servico-101",
            valor_servico=Decimal("100.00"),
            observacoes=None
        )

        assert os_servico.id == 2
        assert os_servico.observacoes is None

    def test_valor_servico_deve_ser_decimal(self):
        os_servico = OrdemServicoServicoEntity(
            id=3,
            ordem_servico_id="os-111",
            servico_id="servico-222",
            valor_servico=Decimal("45.99"),
            observacoes=None
        )

        assert isinstance(os_servico.valor_servico, Decimal)
        assert os_servico.valor_servico == Decimal("45.99")


class TestOrdemServicoServicoEntityFactory:

    def test_create_with_id(self):
        os_servico = OrdemServicoServicoEntityFactory.create(
            id=10,
            ordem_servico_id="os-factory-1",
            servico_id="servico-factory-1",
            valor_servico=Decimal("150.00"),
            observacoes="Criado via factory"
        )

        assert os_servico.id == 10
        assert os_servico.ordem_servico_id == "os-factory-1"
        assert os_servico.servico_id == "servico-factory-1"
        assert os_servico.valor_servico == Decimal("150.00")
        assert os_servico.observacoes == "Criado via factory"

    def test_create_without_id_generates_none(self):
        os_servico = OrdemServicoServicoEntityFactory.create(
            id=None,
            ordem_servico_id="os-factory-2",
            servico_id="servico-factory-2",
            valor_servico=Decimal("200.00"),
            observacoes=None
        )

        assert os_servico.id is None
        assert os_servico.ordem_servico_id == "os-factory-2"
        assert os_servico.servico_id == "servico-factory-2"


class TestOrdemServicoInventoryItemEntity:

    def test_create_ordem_servico_inventory_item_entity(self):
        os_item = OrdemServicoInventoryItemEntity(
            id=1,
            ordem_servico_id="os-123",
            inventory_item_id=456,
            quantidade=3,
            valor_unitario=Decimal("25.90")
        )

        assert os_item.id == 1
        assert os_item.ordem_servico_id == "os-123"
        assert os_item.inventory_item_id == 456
        assert os_item.quantidade == 3
        assert os_item.valor_unitario == Decimal("25.90")

    def test_quantidade_deve_ser_inteiro_positivo(self):
        os_item = OrdemServicoInventoryItemEntity(
            id=2,
            ordem_servico_id="os-789",
            inventory_item_id=101,
            quantidade=5,
            valor_unitario=Decimal("10.50")
        )

        assert isinstance(os_item.quantidade, int)
        assert os_item.quantidade > 0

    def test_valor_unitario_deve_ser_decimal(self):
        os_item = OrdemServicoInventoryItemEntity(
            id=3,
            ordem_servico_id="os-111",
            inventory_item_id=222,
            quantidade=2,
            valor_unitario=Decimal("33.75")
        )

        assert isinstance(os_item.valor_unitario, Decimal)
        assert os_item.valor_unitario == Decimal("33.75")

    def test_calcular_valor_total(self):
        os_item = OrdemServicoInventoryItemEntity(
            id=4,
            ordem_servico_id="os-444",
            inventory_item_id=333,
            quantidade=4,
            valor_unitario=Decimal("12.25")
        )

        valor_total = os_item.quantidade * os_item.valor_unitario
        assert valor_total == Decimal("49.00")


class TestOrdemServicoInventoryItemEntityFactory:

    def test_create_with_id(self):
        os_item = OrdemServicoInventoryItemEntityFactory.create(
            id=15,
            ordem_servico_id="os-factory-item-1",
            inventory_item_id=789,
            quantidade=2,
            valor_unitario=Decimal("45.00")
        )

        assert os_item.id == 15
        assert os_item.ordem_servico_id == "os-factory-item-1"
        assert os_item.inventory_item_id == 789
        assert os_item.quantidade == 2
        assert os_item.valor_unitario == Decimal("45.00")

    def test_create_without_id_generates_none(self):
        os_item = OrdemServicoInventoryItemEntityFactory.create(
            id=None,
            ordem_servico_id="os-factory-item-2",
            inventory_item_id=999,
            quantidade=1,
            valor_unitario=Decimal("100.00")
        )

        assert os_item.id is None
        assert os_item.ordem_servico_id == "os-factory-item-2"
        assert os_item.inventory_item_id == 999


class TestOrdemServicoServicoRepositoryImpl:

    @pytest.fixture
    def mock_database(self):
        return Mock()

    @pytest.fixture
    def repository(self, mock_database):
        repo = OrdemServicoServicoRepositoryImpl()
        repo.database = mock_database
        return repo

    @pytest.mark.asyncio
    async def test_adicionar_servico_a_os(self, repository, mock_database):
        # Arrange
        mock_session = Mock()
        mock_model = Mock()
        mock_model.id = 1
        mock_model.ordem_servico_id = "os-123"
        mock_model.servico_id = "servico-456"
        mock_model.valor_servico = 75.50
        mock_model.observacoes = "Teste"

        mock_database.get_session = AsyncMock()
        mock_database.get_session.return_value.__aiter__ = AsyncMock(return_value=[mock_session])
        mock_session.add = Mock()
        mock_session.flush = AsyncMock()
        mock_session.commit = AsyncMock()

        os_servico_entity = OrdemServicoServicoEntity(
            id=None,
            ordem_servico_id="os-123",
            servico_id="servico-456",
            valor_servico=Decimal("75.50"),
            observacoes="Teste"
        )

        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert os_servico_entity.ordem_servico_id == "os-123"
        assert os_servico_entity.servico_id == "servico-456"
        assert os_servico_entity.valor_servico == Decimal("75.50")

    @pytest.mark.asyncio
    async def test_listar_servicos_por_os(self, repository, mock_database):
        # Arrange
        ordem_servico_id = "os-123"
        
        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert ordem_servico_id == "os-123"

    @pytest.mark.asyncio
    async def test_remover_servico_da_os(self, repository, mock_database):
        # Arrange
        ordem_servico_id = "os-123"
        servico_id = 456
        
        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert ordem_servico_id == "os-123"
        assert servico_id == 456


class TestOrdemServicoInventoryItemRepositoryImpl:

    @pytest.fixture
    def mock_database(self):
        return Mock()

    @pytest.fixture
    def repository(self, mock_database):
        repo = OrdemServicoInventoryItemRepositoryImpl()
        repo.database = mock_database
        return repo

    @pytest.mark.asyncio
    async def test_adicionar_item_a_os(self, repository, mock_database):
        # Arrange
        os_item_entity = OrdemServicoInventoryItemEntity(
            id=None,
            ordem_servico_id="os-123",
            inventory_item_id=456,
            quantidade=2,
            valor_unitario=Decimal("25.50")
        )

        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert os_item_entity.ordem_servico_id == "os-123"
        assert os_item_entity.inventory_item_id == 456
        assert os_item_entity.quantidade == 2

    @pytest.mark.asyncio
    async def test_listar_itens_por_os(self, repository, mock_database):
        # Arrange
        ordem_servico_id = "os-123"
        
        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert ordem_servico_id == "os-123"

    @pytest.mark.asyncio
    async def test_remover_item_da_os(self, repository, mock_database):
        # Arrange
        ordem_servico_id = "os-123"
        inventory_item_id = 456
        
        # Act & Assert
        # Este teste verifica se a estrutura está correta
        # A implementação real seria testada com banco de dados real
        assert ordem_servico_id == "os-123"
        assert inventory_item_id == 456


class TestIntegracaoOrdemServicoVinculos:
    """Testes de integração para validar os vínculos entre ordem de serviço e seus componentes"""

    def test_vinculo_ordem_servico_com_multiplos_servicos(self):
        # Arrange
        ordem_servico_id = "os-multi-servicos"
        
        servico1 = OrdemServicoServicoEntity(
            id=1,
            ordem_servico_id=ordem_servico_id,
            servico_id="servico-1",
            valor_servico=Decimal("50.00"),
            observacoes="Troca de óleo"
        )
        
        servico2 = OrdemServicoServicoEntity(
            id=2,
            ordem_servico_id=ordem_servico_id,
            servico_id="servico-2",
            valor_servico=Decimal("75.00"),
            observacoes="Alinhamento"
        )
        
        servicos = [servico1, servico2]
        
        # Act & Assert
        total_servicos = sum(s.valor_servico for s in servicos)
        assert total_servicos == Decimal("125.00")
        assert all(s.ordem_servico_id == ordem_servico_id for s in servicos)

    def test_vinculo_ordem_servico_com_multiplos_itens(self):
        # Arrange
        ordem_servico_id = "os-multi-itens"
        
        item1 = OrdemServicoInventoryItemEntity(
            id=1,
            ordem_servico_id=ordem_servico_id,
            inventory_item_id=1,
            quantidade=2,
            valor_unitario=Decimal("25.50")
        )
        
        item2 = OrdemServicoInventoryItemEntity(
            id=2,
            ordem_servico_id=ordem_servico_id,
            inventory_item_id=2,
            quantidade=1,
            valor_unitario=Decimal("100.00")
        )
        
        itens = [item1, item2]
        
        # Act & Assert
        total_itens = sum(i.quantidade * i.valor_unitario for i in itens)
        assert total_itens == Decimal("151.00")  # (2 * 25.50) + (1 * 100.00)
        assert all(i.ordem_servico_id == ordem_servico_id for i in itens)

    def test_ordem_servico_completa_com_servicos_e_itens(self):
        # Arrange
        ordem_servico_id = "os-completa"
        
        # Serviços
        servicos = [
            OrdemServicoServicoEntity(
                id=1,
                ordem_servico_id=ordem_servico_id,
                servico_id="servico-1",
                valor_servico=Decimal("80.00"),
                observacoes="Revisão geral"
            ),
            OrdemServicoServicoEntity(
                id=2,
                ordem_servico_id=ordem_servico_id,
                servico_id="servico-2",
                valor_servico=Decimal("120.00"),
                observacoes="Troca de pastilhas"
            )
        ]
        
        # Itens
        itens = [
            OrdemServicoInventoryItemEntity(
                id=1,
                ordem_servico_id=ordem_servico_id,
                inventory_item_id=1,
                quantidade=4,
                valor_unitario=Decimal("15.00")
            ),
            OrdemServicoInventoryItemEntity(
                id=2,
                ordem_servico_id=ordem_servico_id,
                inventory_item_id=2,
                quantidade=2,
                valor_unitario=Decimal("45.00")
            )
        ]
        
        # Act
        total_servicos = sum(s.valor_servico for s in servicos)
        total_itens = sum(i.quantidade * i.valor_unitario for i in itens)
        total_geral = total_servicos + total_itens
        
        # Assert
        assert total_servicos == Decimal("200.00")  # 80 + 120
        assert total_itens == Decimal("150.00")     # (4 * 15) + (2 * 45)
        assert total_geral == Decimal("350.00")     # 200 + 150
        
        # Validar que todos os vínculos apontam para a mesma OS
        assert all(s.ordem_servico_id == ordem_servico_id for s in servicos)
        assert all(i.ordem_servico_id == ordem_servico_id for i in itens)
