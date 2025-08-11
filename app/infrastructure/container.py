from dependency_injector import containers, providers
from app.domain.entities.cliente import ClienteEntityFactory
from app.domain.entities.servico import ServicoEntityFactory
from app.domain.entities.user import UserEntityFactory
from app.infrastructure.database import database
from app.infrastructure.events.cliente import (
    ClienteCreatedQueueEvent,
    ClienteUpdatedQueueEvent,
    ClienteDeletedQueueEvent,
)
from app.infrastructure.events.servico import (
    ServicoCreatedQueueEvent,
    ServicoUpdatedQueueEvent,
    ServicoDeletedQueueEvent,
)
from app.infrastructure.events.user_events import (
    UserCreatedQueueEvent,
    UserUpdatedQueueEvent,
    UserDeletedQueueEvent,
)

from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.use_cases.user_use_case import UserUseCases
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.infrastructure.handlers import Handlers
from app.application.services.cliente import ClienteService
from app.application.services.servico import ServicoService
from app.application.services.user_service import UserService
from app.application.services.password_service import PasswordService


class Container(containers.DeclarativeContainer):

    #loads all handlers where @injects are set
    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())
    db_session = providers.Resource(database.get_session)

    # Factories
    cliente_factory = providers.Factory(ClienteEntityFactory)
    servico_factory = providers.Factory(ServicoEntityFactory)
    user_factory = providers.Factory(UserEntityFactory)
    

    # Repositories
    cliente_repository = providers.Singleton(ClienteRepositoryImpl)
    servico_repository = providers.Singleton(ServicoRepositoryImpl)
    user_repository = providers.Singleton(UserRepositoryImpl)

    # Events

    cliente_created_event = providers.Factory(ClienteCreatedQueueEvent)
    cliente_updated_event = providers.Factory(ClienteUpdatedQueueEvent)
    cliente_deleted_event = providers.Factory(ClienteDeletedQueueEvent)

    servico_created_event = providers.Factory(ServicoCreatedQueueEvent)
    servico_updated_event = providers.Factory(ServicoUpdatedQueueEvent)
    servico_deleted_event = providers.Factory(ServicoDeletedQueueEvent)

    user_created_event = providers.Factory(UserCreatedQueueEvent)
    user_updated_event = providers.Factory(UserUpdatedQueueEvent)
    user_deleted_event = providers.Factory(UserDeletedQueueEvent)

    # Services

    password_service = providers.Singleton(
        PasswordService,
    )
    cliente_service = providers.Factory(
        ClienteService,
        cliente_repository,
        cliente_created_event,
        cliente_updated_event,
        cliente_deleted_event,
    )
    servico_service = providers.Factory(
        ServicoService,
        servico_repository,
        servico_created_event,
        servico_updated_event,
        servico_deleted_event,
    )
    user_service = providers.Factory(
        UserService,
        user_repository,
        password_service,
        user_created_event,
        user_updated_event,
        user_deleted_event,
    )

    # Repositories - recebem a sessão do db
    inventory_item_repository = providers.Factory(
        InventoryItemRepositoryImpl,
        db=db_session
    )
    vehicle_repository = providers.Factory(
        VehicleRepositoryImpl,
        db=db_session
    )

    # Use Cases recebem os repositórios
    inventory_item_use_case = providers.Factory(
        InventoryItemUseCase,
        repository=inventory_item_repository
    )
    vehicle_use_case = providers.Factory(
        VehicleUseCase,
        repository=vehicle_repository
    )
