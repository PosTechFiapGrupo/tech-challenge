import pytest
from unittest.mock import AsyncMock, MagicMock
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.entities.user import UserEntityFactory


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
    repo = UserRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
async def test_get_all(repo, mock_session):
    user_model_1 = MagicMock(
        id=1,
        nome="User1",
        email="user1@example.com",
        hashed_password="hashed123",
        funcao="admin",
        criado_em=None,
        atualizado_em=None,
    )
    user_model_2 = MagicMock(
        id=2,
        nome="User2",
        email="user2@example.com",
        hashed_password="hashed123",
        funcao="user",
        criado_em=None,
        atualizado_em=None,
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [user_model_1, user_model_2]
    mock_session.execute.return_value = mock_result

    users = await repo.get_all()

    mock_session.execute.assert_awaited_once()
    assert len(users) == 2
    assert users[0].id == str(user_model_1.id)
    assert users[1].email == "user2@example.com"


@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_session):
    user_model = MagicMock(
        id=1,
        nome="User1",
        email="user1@example.com",
        hashed_password="hashed123",
        funcao="admin",
        criado_em=None,
        atualizado_em=None,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user_model
    mock_session.execute.return_value = mock_result

    user = await repo.get_by_id("1")

    mock_session.execute.assert_awaited_once()
    assert user is not None
    assert user.id == str(user_model.id)
    assert user.nome == user_model.nome


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    user = await repo.get_by_id("999")

    mock_session.execute.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_get_by_email_found(repo, mock_session):
    user_model = MagicMock(
        id=1,
        nome="User1",
        email="user1@example.com",
        hashed_password="hashed123",
        funcao="admin",
        criado_em=None,
        atualizado_em=None,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user_model
    mock_session.execute.return_value = mock_result

    user = await repo.get_by_email("USER1@example.com")

    mock_session.execute.assert_awaited_once()
    assert user is not None
    assert user.email == user_model.email


@pytest.mark.asyncio
async def test_get_by_email_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    user = await repo.get_by_email("notfound@example.com")

    mock_session.execute.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_add_success(repo, mock_session):
    user_entity = UserEntityFactory.create(
        id=None,
        nome="New User",
        email="newuser@example.com",
        hashed_password="hashedpass",
        funcao="user",
        criado_em=None,
        atualizado_em=None,
    )

    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.refresh.return_value = None
    mock_session.commit.return_value = None

    # Simula side effect do refresh para setar id
    async def refresh_side_effect(obj):
        obj.id = 10
    mock_session.refresh.side_effect = refresh_side_effect

    user = await repo.add(user_entity)

    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

    assert user.id == "10"
    assert user.nome == "New User"


@pytest.mark.asyncio
async def test_update_success(repo, mock_session):
    user_entity = UserEntityFactory.create(
        id="1",
        nome="Updated User",
        email="updated@example.com",
        hashed_password="hashedpass",
        funcao="admin",
        criado_em=None,
        atualizado_em=None,
    )

    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    user = await repo.update(user_entity)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

    assert user.nome == "Updated User"


@pytest.mark.asyncio
async def test_update_not_found(repo, mock_session):
    user_entity = UserEntityFactory.create(
        id="999",
        nome="No User",
        email="nouser@example.com",
        hashed_password="hashedpass",
        funcao="user",
        criado_em=None,
        atualizado_em=None,
    )

    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute.return_value = mock_result

    with pytest.raises(ValueError):
        await repo.update(user_entity)

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
