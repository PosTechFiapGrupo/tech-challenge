from dependency_injector import containers, providers

from app.application.validators import vehicle_validator
from app.infrastructure.database import database
from app.infrastructure.handlers import Handlers

# Entities
from app.domain.entities.cliente import ClienteEntityFactory
from app.domain.entities.servico import ServicoEntityFactory
from app.domain.entities.user import UserEntityFactory
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory

# Repositories
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.infrastructure.repositories.ordem_servico_impl import OrdemServicoRepositoryImpl
from app.infrastructure.events.user_events import (
    UserCreatedQueueEvent,
    UserUpdatedQueueEvent,
    UserDeletedQueueEvent,
)

from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl
from app.infrastructure.repositories.ordem_servico_servico_impl import OrdemServicoServicoRepositoryImpl
from app.infrastructure.repositories.ordem_servico_inventory_item_impl import OrdemServicoInventoryItemRepositoryImpl

# Events
from app.infrastructure.events.cliente import ClienteCreatedQueueEvent, ClienteUpdatedQueueEvent, ClienteDeletedQueueEvent
from app.infrastructure.events.servico import ServicoCreatedQueueEvent, ServicoUpdatedQueueEvent, ServicoDeletedQueueEvent
from app.infrastructure.events.ordem_servico import (
    OrdemServicoSolicitadaQueueEvent,
    OrcamentoSolicitadoQueueEvent,
    MecanicoDesignadoQueueEvent,
    ServicosIncluidosQueueEvent,
    PecaOuInsumoIncluidoQueueEvent,
    OrcamentoGeradoQueueEvent,
    OrcamentoEnviadoAoClienteQueueEvent,
    OrdemServicoAceitaQueueEvent,
    OrdemServicoRealizadaQueueEvent,
)

# Validators
from app.application.validators.cliente import ClienteValidator
from app.application.validators.servico import ServicoValidator
from app.application.validators.ordem_servico import OrdemServicoValidator
from app.application.validators.veiculo import VeiculoValidator

# Use Cases
from app.domain.use_cases.ordem_servico_impl import OrdemServicoUseCasesImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.use_cases.vehicle_use_case import VehicleUseCase

# Services
from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.use_cases.user_use_case import UserUseCases
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.infrastructure.handlers import Handlers
from app.application.services.cliente import ClienteService
from app.application.services.servico import ServicoService
from app.application.services.ordem_servico import OrdemServicoService
from app.application.services.vehicle import VehicleService
from app.application.services.orcamento import OrcamentoService
from app.application.services.user_service import UserService
from app.application.services.password_service import PasswordService

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())
    db_session = providers.Resource(database.get_session)

    # Factories
    cliente_factory = providers.Factory(ClienteEntityFactory)
    servico_factory = providers.Factory(ServicoEntityFactory)
    user_factory = providers.Factory(UserEntityFactory)
    ordem_servico_factory = providers.Factory(OrdemServicoEntityFactory)

    # Repositories
    cliente_repository = providers.Singleton(ClienteRepositoryImpl)
    servico_repository = providers.Singleton(ServicoRepositoryImpl)
    ordem_servico_repository = providers.Singleton(OrdemServicoRepositoryImpl)
    inventory_item_repository = providers.Factory(InventoryItemRepositoryImpl, db=db_session)
    vehicle_repository = providers.Factory(VehicleRepositoryImpl, db=db_session)
    ordem_servico_servico_repository = providers.Singleton(OrdemServicoServicoRepositoryImpl)
    ordem_servico_inventory_item_repository = providers.Singleton(OrdemServicoInventoryItemRepositoryImpl)
    user_repository = providers.Singleton(UserRepositoryImpl)

    # Events
    cliente_created_event = providers.Factory(ClienteCreatedQueueEvent)
    cliente_updated_event = providers.Factory(ClienteUpdatedQueueEvent)
    cliente_deleted_event = providers.Factory(ClienteDeletedQueueEvent)
    servico_created_event = providers.Factory(ServicoCreatedQueueEvent)
    servico_updated_event = providers.Factory(ServicoUpdatedQueueEvent)
    servico_deleted_event = providers.Factory(ServicoDeletedQueueEvent)
    ordem_servico_solicitada_event = providers.Factory(OrdemServicoSolicitadaQueueEvent)
    orcamento_solicitado_event = providers.Factory(OrcamentoSolicitadoQueueEvent)
    mecanico_designado_event = providers.Factory(MecanicoDesignadoQueueEvent)
    servicos_incluidos_event = providers.Factory(ServicosIncluidosQueueEvent)
    peca_ou_insumo_incluido_event = providers.Factory(PecaOuInsumoIncluidoQueueEvent)
    orcamento_gerado_event = providers.Factory(OrcamentoGeradoQueueEvent)
    orcamento_enviado_ao_cliente_event = providers.Factory(OrcamentoEnviadoAoClienteQueueEvent)
    ordem_servico_aceita_event = providers.Factory(OrdemServicoAceitaQueueEvent)
    ordem_servico_realizada_event = providers.Factory(OrdemServicoRealizadaQueueEvent)
    user_created_event = providers.Factory(UserCreatedQueueEvent)
    user_updated_event = providers.Factory(UserUpdatedQueueEvent)
    user_deleted_event = providers.Factory(UserDeletedQueueEvent)

    # Validators
    cliente_validator = providers.Singleton(ClienteValidator, cliente_repository)
    servico_validator = providers.Singleton(ServicoValidator, servico_repository)
    ordem_servico_validator = providers.Singleton(
        OrdemServicoValidator,
        cliente_repository=cliente_repository,
        servico_repository=servico_repository,
    )
    vehicle_validator = providers.Factory(
        VeiculoValidator, vehicle_repository=vehicle_repository
    )

    # Use Cases
    ordem_servico_use_case = providers.Factory(
        OrdemServicoUseCasesImpl,
        ordem_servico_repository=ordem_servico_repository,
        os_criada_event=ordem_servico_solicitada_event,
        orcamento_solicitado_event=orcamento_solicitado_event,
        mecanico_designado_event=mecanico_designado_event,
        servicos_incluidos_event=servicos_incluidos_event,
        peca_incluida_event=peca_ou_insumo_incluido_event,
        orcamento_gerado_event=orcamento_gerado_event,
        orcamento_enviado_event=orcamento_enviado_ao_cliente_event,
        os_aceita_event=ordem_servico_aceita_event,
        os_realizada_event=ordem_servico_realizada_event,
    )

    inventory_item_use_case = providers.Factory(
        InventoryItemUseCase, repository=inventory_item_repository
    )
    vehicle_use_case = providers.Factory(
        VehicleUseCase, repository=vehicle_repository
    )

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

    ordem_servico_service = providers.Factory(
        OrdemServicoService,
        use_case=ordem_servico_use_case,
        cliente_validator=cliente_validator,
        servico_validator=servico_validator,
        vehicle_validator=vehicle_validator,
        ordem_servico_validator=ordem_servico_validator,
        servico_use_case=servico_service,
        inventory_item_use_case=inventory_item_use_case,
        os_servico_repository=ordem_servico_servico_repository,
        os_item_repository=ordem_servico_inventory_item_repository,
      
    vehicle_service = providers.Factory(
        VehicleService,
        use_case=vehicle_use_case,
        vehicle_validator=vehicle_validator,
    )
    orcamento_service = providers.Factory(
        OrcamentoService,
        ordem_servico_repository=ordem_servico_repository,
        servico_repository=servico_repository,
        inventory_repository=inventory_item_repository,
        os_servico_repository=ordem_servico_servico_repository,
        os_inventory_repository=ordem_servico_inventory_item_repository,
    )