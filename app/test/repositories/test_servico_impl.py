import pytest
from unittest.mock import AsyncMock, MagicMock
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.domain.entities.servico import ServicoEntityFactory


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
    repo = ServicoRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
async def test_get_all(repo, mock_session):
    servico1 = MagicMock(id=1, descricao="Serviço 1", preco=100.0)
    servico2 = MagicMock(id=2, descricao="Serviço 2", preco=200.0)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [servico1, servico2]
    mock_session.execute.return_value = mock_result

    servicos = await repo.get_all()

    mock_session.execute.assert_awaited_once()
    assert len(servicos) == 2
    assert servicos[0].id == str(servico1.id)
    assert servicos[1].descricao == "Serviço 2"
    assert servicos[1].preco == 200.0


@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_session):
    servico = MagicMock(id=1, descricao="Serviço 1", preco=100.0)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = servico
    mock_session.execute.return_value = mock_result

    result = await repo.get_by_id("1")

    mock_session.execute.assert_awaited_once()
    assert result is not None
    assert result.id == str(servico.id)
    assert result.descricao == servico.descricao
    assert result.preco == float(servico.preco)


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await repo.get_by_id("999")

    mock_session.execute.assert_awaited_once()
    assert result is None


@pytest.mark.asyncio
async def test_add_success(repo, mock_session):
    servico_entity = ServicoEntityFactory.create(
        id=None,
        descricao="Novo Serviço",
        preco=123.45,
    )

    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.refresh.return_value = None
    mock_session.commit.return_value = None

    async def refresh_side_effect(obj):
        obj.id = 10

    mock_session.refresh.side_effect = refresh_side_effect

    result = await repo.add(servico_entity)

    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

    assert result.id == "10"
    assert result.descricao == "Novo Serviço"
    assert result.preco == 123.45


@pytest.mark.asyncio
async def test_update_success(repo, mock_session):
    servico_entity = ServicoEntityFactory.create(
        id="1",
        descricao="Serviço Atualizado",
        preco=999.99,
    )

    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    result = await repo.update(servico_entity)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert result.descricao == "Serviço Atualizado"
    assert result.preco == 999.99


@pytest.mark.asyncio
async def test_update_not_found(repo, mock_session):
    servico_entity = ServicoEntityFactory.create(
        id="999",
        descricao="Não Existe",
        preco=999.99,
    )

    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result

    with pytest.raises(ValueError):
        await repo.update(servico_entity)

    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_success(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    result = await repo.delete("1")

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert result is True


@pytest.mark.asyncio
async def test_delete_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result

    result = await repo.delete("999")

    mock_session.execute.assert_awaited_once()
    assert result is False
