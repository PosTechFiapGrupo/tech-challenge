import pytest
from unittest.mock import AsyncMock, Mock
from app.application.services.user_service import UserService
from app.domain.entities.user import UserEntity, UserFuncao
from app.domain.exceptions import InvalidEmail


class TestUserService:

    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()

    @pytest.fixture
    def mock_created_event(self):
        m = Mock()
        m.send = Mock()
        return m

    @pytest.fixture
    def mock_updated_event(self):
        m = Mock()
        m.send = Mock()
        return m

    @pytest.fixture
    def mock_deleted_event(self):
        m = Mock()
        m.send = Mock()
        return m
    
    @pytest.fixture
    def mock_user_deleted_event(self):
        m = Mock()
        m.send = Mock()
        return m

    @pytest.fixture
    def user_service(
        self,
        mock_repository,
        mock_created_event,
        mock_updated_event,
        mock_deleted_event,
        mock_user_deleted_event
    ):
        return UserService(
            mock_repository,
            password_service=Mock(hash_password=lambda pw: "hashed_" + pw),
            user_created_event=mock_created_event,
            user_updated_event=mock_updated_event,
            user_deleted_event=mock_user_deleted_event,
        )

    @pytest.fixture
    def sample_user(self):
        return UserEntity(
            "1",
            "Maria Souza",
            "maria@example.com",
            "hashed_password",
            UserFuncao.CLIENTE
        )

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_service, mock_repository, sample_user):
        mock_repository.get_all.return_value = [sample_user]

        result = await user_service.get_all_users()

        assert len(result) == 1
        assert result[0].nome == "Maria Souza"
        mock_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user_service, mock_repository, sample_user):
        mock_repository.get_by_id.return_value = sample_user

        result = await user_service.get_user_by_id("1")

        assert result.nome == "Maria Souza"
        mock_repository.get_by_id.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_create_user(
        self, user_service, mock_repository, mock_created_event, sample_user
    ):
        mock_repository.add.return_value = sample_user

        result = await user_service.create_user(sample_user, plain_password="senha123")

        assert result.nome == "Maria Souza"
        mock_repository.add.assert_called_once_with(sample_user)
        mock_created_event.send.assert_called_once_with(sample_user)

    @pytest.mark.asyncio
    async def test_create_user_with_invalid_email(self, user_service):
        with pytest.raises(InvalidEmail):
            user = UserEntity(
                "1", "Maria Souza", "email-invalido", "hashed_password", UserFuncao.CLIENTE
            )
            await user_service.create_user(user, plain_password="senha123")
