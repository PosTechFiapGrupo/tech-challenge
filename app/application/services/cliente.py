from typing import List

from app.application.validators.cliente import ClienteValidator
from app.domain.entities.cliente import ClienteEntity
from app.domain.events.cliente import (
    ClienteCreatedEvent,
    ClienteDeletedEvent,
    ClienteUpdatedEvent,
)
from app.domain.repositories.cliente import ClienteRepository
from app.domain.use_cases.cliente import ClienteUseCases
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class ClienteService(ClienteUseCases):

    def __init__(
        self,
        cliente_repository: ClienteRepository,
        cliente_created_event: ClienteCreatedEvent,
        cliente_updated_event: ClienteUpdatedEvent,
        cliente_deleted_event: ClienteDeletedEvent,
    ):
        super().__init__(
            cliente_repository,
            cliente_created_event,
            cliente_updated_event,
            cliente_deleted_event,
        )

    async def get_all_clientes(self) -> List[ClienteEntity]:
        clientes = await self.cliente_repository.get_all()
        logger.info("Clientes listados", extra={"count": len(clientes)})
        return clientes

    async def get_cliente_by_id(self, id: str) -> ClienteEntity | None:
        cliente = await self.cliente_repository.get_by_id(id)
        logger.info("Cliente buscado por ID", extra={"cliente_id": id, "found": cliente is not None})
        return cliente

    async def get_cliente_by_cpf(self, cpf: str) -> ClienteEntity | None:
        cliente = await self.cliente_repository.get_by_cpf(cpf)
        logger.info("Cliente buscado por CPF", extra={"found": cliente is not None})
        return cliente

    async def create_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        ClienteValidator.validate_nome(cliente.nome)
        ClienteValidator.validate_email(cliente.email)
        ClienteValidator.validate_cpf(cliente.cpf)
        ClienteValidator.validate_phone(cliente.telefone)

        created_cliente = await self.cliente_repository.add(cliente)
        self.cliente_created_event.send(created_cliente)
        logger.info("Cliente criado", extra={"cliente_id": str(created_cliente.id), "email": cliente.email})
        return created_cliente

    async def update_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        ClienteValidator.validate_nome(cliente.nome)
        ClienteValidator.validate_email(cliente.email)
        ClienteValidator.validate_cpf(cliente.cpf)
        ClienteValidator.validate_phone(cliente.telefone)

        updated_cliente = await self.cliente_repository.update(cliente)
        self.cliente_updated_event.send(updated_cliente)
        logger.info("Cliente atualizado", extra={"cliente_id": str(cliente.id)})
        return updated_cliente

    async def delete_cliente(self, id: str) -> bool:
        result = await self.cliente_repository.delete(id)
        if result:
            self.cliente_deleted_event.send(id)
            logger.info("Cliente deletado", extra={"cliente_id": id})
        else:
            logger.warning("Falha ao deletar cliente", extra={"cliente_id": id})
        return result
