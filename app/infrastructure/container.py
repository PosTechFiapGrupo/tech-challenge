from dependency_injector import containers, providers
from app.infrastructure.database import database
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.infrastructure.handlers import Handlers

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())

    # Resource provider for DB session (async context manager)
    db_session = providers.Resource(database.get_session)

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
