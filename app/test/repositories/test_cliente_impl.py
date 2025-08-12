import pytest
from unittest.mock import AsyncMock, MagicMock
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.models.cliente import ClienteModel
from app.domain.entities.cliente import ClienteEntity, ClienteEntityFactory


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
    session = AsyncMock()
    # mocks básicos para session
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def mock_database(mock_session):
    db = MagicMock()
    db.get_session.return_value = AsyncSessionIterator(mock_session)
    return db


@pytest.fixture
def repo(mock_database):
    repo = ClienteRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
async def test_get_all(repo, mock_session):
    cliente1 = MagicMock(id=1, nome="Cliente1", telefone="1234567891", email="c1@test.com", cpf="12345678910")
    cliente2 = MagicMock(id=2, nome="Cliente2", telefone="1234567891", email="c2@test.com", cpf="12345678910")
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [cliente1, cliente2]
    mock_session.execute.return_value = mock_result

    clientes = await repo.get_all()

    mock_session.execute.assert_awaited_once()
    assert len(clientes) == 2
    assert clientes[0].nome == "Cliente1"
    assert clientes[1].cpf == "12345678910"


@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_session):
    cliente = MagicMock(id=1, nome="Cliente1", telefone="1234567891", email="c1@test.com", cpf="12345678910")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = cliente
    mock_session.execute.return_value = mock_result

    cliente_entity = await repo.get_by_id("1")

    mock_session.execute.assert_awaited_once()
    assert cliente_entity is not None
    assert cliente_entity.id == "1"
    assert cliente_entity.nome == "Cliente1"


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    cliente_entity = await repo.get_by_id("999")

    mock_session.execute.assert_awaited_once()
    assert cliente_entity is None


@pytest.mark.asyncio
async def test_get_by_cpf_found(repo, mock_session):
    cliente = MagicMock(id=1, nome="Cliente1", telefone="1234567891", email="c1@test.com", cpf="12345678900")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = cliente
    mock_session.execute.return_value = mock_result

    cliente_entity = await repo.get_by_cpf("123.456.789-00")

    mock_session.execute.assert_awaited_once()
    assert cliente_entity is not None
    assert cliente_entity.cpf == "12345678900"


@pytest.mark.asyncio
async def test_get_by_cpf_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    cliente_entity = await repo.get_by_cpf("000.000.000-00")

    mock_session.execute.assert_awaited_once()
    assert cliente_entity is None


@pytest.mark.asyncio
async def test_add(repo, mock_session):
    cliente_entity = ClienteEntityFactory.create(id=None, nome="Novo", telefone="1234567891", email="novo@test.com", cpf="11122233344")
    cliente_model = MagicMock()
    cliente_model.id = 10

    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.refresh.return_value = None
    mock_session.commit.return_value = None

    async def refresh_side_effect(obj):
        obj.id = 10

    mock_session.refresh.side_effect = refresh_side_effect

    result = await repo.add(cliente_entity)

    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

    assert result.id == "10"
    assert result.nome == "Novo"


@pytest.mark.asyncio
async def test_update_success(repo, mock_session):
    cliente_entity = ClienteEntityFactory.create(id="1", nome="Atualizado", telefone="1234567891", email="upd@test.com", cpf="55566677788")

    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    result = await repo.update(cliente_entity)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert result.nome == "Atualizado"


@pytest.mark.asyncio
async def test_update_not_found(repo, mock_session):
    cliente_entity = ClienteEntityFactory.create(id="999", nome="Não Existe", telefone="1234567891", email="no@test.com", cpf="00000000000")

    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result

    with pytest.raises(ValueError):
        await repo.update(cliente_entity)

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
