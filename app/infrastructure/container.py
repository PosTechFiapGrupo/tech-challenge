from dependency_injector import containers, providers
from app.domain.entities.product import ProductEntityFactory
from app.domain.entities.cliente import ClienteEntityFactory
from app.domain.entities.servico import ServicoEntityFactory
from app.infrastructure.events.product import (
    ProductCreatedQueueEvent,
    ProductUpdatedQueueEvent,
)
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
from app.infrastructure.handlers import Handlers
from app.infrastructure.repositories.product_impl import ProductRepositoryImpl
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.application.services.product import ProductService
from app.application.services.cliente import ClienteService
from app.application.services.servico import ServicoService


class Container(containers.DeclarativeContainer):

    # loads all handlers where @injects are set
    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())

    # Factories
    product_factory = providers.Factory(ProductEntityFactory)
    cliente_factory = providers.Factory(ClienteEntityFactory)
    servico_factory = providers.Factory(ServicoEntityFactory)

    # Repositories
    product_repository = providers.Singleton(ProductRepositoryImpl)
    cliente_repository = providers.Singleton(ClienteRepositoryImpl)
    servico_repository = providers.Singleton(ServicoRepositoryImpl)

    # Events
    product_created_event = providers.Factory(ProductCreatedQueueEvent)
    product_updated_event = providers.Factory(ProductUpdatedQueueEvent)

    cliente_created_event = providers.Factory(ClienteCreatedQueueEvent)
    cliente_updated_event = providers.Factory(ClienteUpdatedQueueEvent)
    cliente_deleted_event = providers.Factory(ClienteDeletedQueueEvent)

    servico_created_event = providers.Factory(ServicoCreatedQueueEvent)
    servico_updated_event = providers.Factory(ServicoUpdatedQueueEvent)
    servico_deleted_event = providers.Factory(ServicoDeletedQueueEvent)

    # Services
    product_services = providers.Factory(
        ProductService, product_repository, product_created_event, product_updated_event
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
