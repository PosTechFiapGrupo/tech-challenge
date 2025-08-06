from dependency_injector import containers, providers

from app.infrastructure.database import database
from app.infrastructure.handlers import Handlers

from app.domain.entities.cliente import ClienteEntityFactory
from app.domain.entities.servico import ServicoEntityFactory
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory

from app.infrastructure.repositories.cliente_impl import ClienteRepositoryImpl
from app.infrastructure.repositories.servico_impl import ServicoRepositoryImpl
from app.infrastructure.repositories.ordem_servico_impl import OrdemServicoRepositoryImpl
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.infrastructure.repositories.vehicle_repository_impl import VehicleRepositoryImpl

from app.infrastructure.events.product import ProductCreatedQueueEvent, ProductUpdatedQueueEvent
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

from app.application.validators.cliente import ClienteValidator
from app.application.validators.servico import ServicoValidator
from app.application.validators.ordem_servico import OrdemServicoValidator

from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.domain.use_cases.ordem_servico_impl import OrdemServicoUseCasesImpl

from app.application.services.cliente import ClienteService
from app.application.services.servico import ServicoService
from app.application.services.ordem_servico import OrdemServicoService


class Container(containers.DeclarativeContainer):

    # loads all handlers where @injects are set
    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())
    db_session = providers.Resource(database.get_session)

    # Factories
    cliente_factory = providers.Factory(ClienteEntityFactory)
    servico_factory = providers.Factory(ServicoEntityFactory)
    ordem_servico_factory = providers.Factory(OrdemServicoEntityFactory)

    # Repositories
    cliente_repository = providers.Singleton(ClienteRepositoryImpl)
    servico_repository = providers.Singleton(ServicoRepositoryImpl)
    ordem_servico_repository = providers.Singleton(OrdemServicoRepositoryImpl)

    # Events
    product_created_event = providers.Factory(ProductCreatedQueueEvent)
    product_updated_event = providers.Factory(ProductUpdatedQueueEvent)

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

    # Validators
    cliente_validator = providers.Singleton(ClienteValidator)
    servico_validator = providers.Singleton(ServicoValidator)
    ordem_servico_validator = providers.Singleton(
        OrdemServicoValidator,
        cliente_repository=cliente_repository,
        servico_repository=servico_repository,
    )

    # Use Cases
    ordem_servico_use_case = providers.Factory(
        OrdemServicoUseCasesImpl,
        repository=ordem_servico_repository,
        factory=ordem_servico_factory,
        ordem_servico_solicitada_event=ordem_servico_solicitada_event,
        orcamento_solicitado_event=orcamento_solicitado_event,
        mecanico_designado_event=mecanico_designado_event,
        servicos_incluidos_event=servicos_incluidos_event,
        peca_ou_insumo_incluido_event=peca_ou_insumo_incluido_event,
        orcamento_gerado_event=orcamento_gerado_event,
        orcamento_enviado_ao_cliente_event=orcamento_enviado_ao_cliente_event,
        ordem_servico_aceita_event=ordem_servico_aceita_event,
        ordem_servico_realizada_event=ordem_servico_realizada_event,
    )

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
    ordem_servico_service = providers.Factory(
        OrdemServicoService,
        use_case=ordem_servico_use_case,
        cliente_validator=cliente_validator,
        servico_validator=servico_validator,
        ordem_servico_validator=ordem_servico_validator,
    )