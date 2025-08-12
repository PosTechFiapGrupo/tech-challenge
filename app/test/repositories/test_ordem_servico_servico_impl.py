import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from datetime import timedelta
from app.infrastructure.repositories.ordem_servico_servico_impl import OrdemServicoServicoRepositoryImpl
from app.domain.entities.ordem_servico_servico import OrdemServicoServicoEntity

# Async iterator para simular `async for session in database.get_session()`
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
    repo = OrdemServicoServicoRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
async def test_adicionar_servico_a_os(repo, mock_session):
    # mock do add para modificar o objeto passado (simulando auto-increment do id)
    def add_side_effect(model):
        model.id = 123
        model.ordem_servico_id = "os1"
        model.servico_id = 10
        model.valor_servico = Decimal("150.75")
        model.observacoes = "teste obs"

    mock_session.add.side_effect = add_side_effect
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    os_servico_entity = OrdemServicoServicoEntity(
        id=None,
        ordem_servico_id="os1",
        servico_id=10,
        valor_servico=Decimal("150.75"),
        observacoes="teste obs"
    )

    result = await repo.adicionar_servico_a_os(os_servico_entity)

    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert result.id == None
    assert result.valor_servico == Decimal("150.75")


@pytest.mark.asyncio
async def test_listar_servicos_por_os(repo, mock_session):
    model_1 = MagicMock()
    model_1.id = 1
    model_1.ordem_servico_id = "os1"
    model_1.servico_id = 10
    model_1.valor_servico = Decimal("100")
    model_1.observacoes = "obs1"

    model_2 = MagicMock()
    model_2.id = 2
    model_2.ordem_servico_id = "os1"
    model_2.servico_id = 20
    model_2.valor_servico = Decimal("200")
    model_2.observacoes = "obs2"

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [model_1, model_2]
    mock_session.execute.return_value = mock_result

    servicos = await repo.listar_servicos_por_os("os1")

    mock_session.execute.assert_awaited_once()
    assert len(servicos) == 2
    assert servicos[0].id == 1
    assert servicos[1].valor_servico == Decimal("200")


@pytest.mark.asyncio
async def test_remover_servico_da_os_success(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    result = await repo.remover_servico_da_os("os1", 10)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert result is True


@pytest.mark.asyncio
async def test_remover_servico_da_os_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result

    result = await repo.remover_servico_da_os("os1", 999)

    mock_session.execute.assert_awaited_once()
    assert result is False


@pytest.mark.asyncio
async def test_calcular_tempo_medio_execucao_com_result(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = 3600.0  # 1 hora em segundos
    mock_session.execute.return_value = mock_result

    resultado = await repo.calcular_tempo_medio_execucao()

    mock_session.execute.assert_awaited_once()
    assert resultado == timedelta(seconds=3600)


@pytest.mark.asyncio
async def test_calcular_tempo_medio_execucao_sem_result(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = None
    mock_session.execute.return_value = mock_result

    resultado = await repo.calcular_tempo_medio_execucao()

    mock_session.execute.assert_awaited_once()
    assert resultado is None
