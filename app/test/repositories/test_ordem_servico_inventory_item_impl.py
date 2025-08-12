import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from app.infrastructure.repositories.ordem_servico_inventory_item_impl import OrdemServicoInventoryItemRepositoryImpl
from app.domain.entities.ordem_servico_inventory_item import OrdemServicoInventoryItemEntity

# Async iterator para simular `async for` ou o uso manual de __anext__ em get_session()
class AsyncSessionIterator:
    def __init__(self, session):
        self.session = session
        self._yielded = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._yielded:
            self._yielded = True
            return self.session
        else:
            raise StopAsyncIteration


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def mock_database(mock_session):
    db = MagicMock()
    db.get_session.return_value = AsyncSessionIterator(mock_session)
    return db


@pytest.fixture
def repo(mock_database):
    repo = OrdemServicoInventoryItemRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
async def test_adicionar_item_a_os(repo, mock_session):
    # Simula side effect do add para setar atributos no model
    def add_side_effect(model):
        model.id = 42
        model.ordem_servico_id = "os123"
        model.inventory_item_id = 7
        model.quantidade = 5
        model.valor_unitario = Decimal("12.34")

    mock_session.add.side_effect = add_side_effect
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None

    entity = OrdemServicoInventoryItemEntity(
        id=None,
        ordem_servico_id="os123",
        inventory_item_id=7,
        quantidade=5,
        valor_unitario=Decimal("12.34"),
    )

    result = await repo.adicionar_item_a_os(entity)

    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.close.assert_awaited_once()

    assert result.id == None
    assert result.ordem_servico_id == "os123"
    assert result.quantidade == 5
    assert result.valor_unitario == Decimal("12.34")


@pytest.mark.asyncio
async def test_listar_itens_por_os(repo, mock_session):
    model_1 = MagicMock()
    model_1.id = 1
    model_1.ordem_servico_id = "os123"
    model_1.inventory_item_id = 5
    model_1.quantidade = 10
    model_1.valor_unitario = Decimal("100.00")

    model_2 = MagicMock()
    model_2.id = 2
    model_2.ordem_servico_id = "os123"
    model_2.inventory_item_id = 6
    model_2.quantidade = 3
    model_2.valor_unitario = Decimal("50.50")

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [model_1, model_2]
    mock_session.execute.return_value = mock_result
    mock_session.close.return_value = None

    items = await repo.listar_itens_por_os("os123")

    mock_session.execute.assert_awaited_once()
    mock_session.close.assert_awaited_once()

    assert len(items) == 2
    assert items[0].id == 1
    assert items[0].quantidade == 10
    assert items[1].valor_unitario == Decimal("50.50")


@pytest.mark.asyncio
async def test_remover_item_da_os_success(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None

    result = await repo.remover_item_da_os("os123", 5)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.close.assert_awaited_once()

    assert result is True


@pytest.mark.asyncio
async def test_remover_item_da_os_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result
    mock_session.close.return_value = None

    result = await repo.remover_item_da_os("os123", 999)

    mock_session.execute.assert_awaited_once()
    mock_session.close.assert_awaited_once()

    assert result is False