from dependency_injector import containers, providers
from app.domain.entities.cliente import ClienteEntityFactory
from app.domain.entities.servico import ServicoEntityFactory
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
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.infrastructure.handlers import Handlers
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.application.services.cliente import ClienteService
from app.application.services.servico import ServicoService


class Container(containers.DeclarativeContainer):

    #loads all handlers where @injects are set
    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())
    db_session = providers.Resource(database.get_session)

    # Factories
    cliente_factory = providers.Factory(ClienteEntityFactory)
    servico_factory = providers.Factory(ServicoEntityFactory)
    

    # Repositories
    cliente_repository = providers.Singleton(ClienteRepositoryImpl)
    servico_repository = providers.Singleton(ServicoRepositoryImpl)

    # Events

    cliente_created_event = providers.Factory(ClienteCreatedQueueEvent)
    cliente_updated_event = providers.Factory(ClienteUpdatedQueueEvent)
    cliente_deleted_event = providers.Factory(ClienteDeletedQueueEvent)

    servico_created_event = providers.Factory(ServicoCreatedQueueEvent)
    servico_updated_event = providers.Factory(ServicoUpdatedQueueEvent)
    servico_deleted_event = providers.Factory(ServicoDeletedQueueEvent)

    # Services

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
