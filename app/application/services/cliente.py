from typing import List
from app.domain.use_cases.cliente import ClienteUseCases
from app.domain.entities.cliente import ClienteEntity
from app.domain.events.cliente import (
    ClienteCreatedEvent,
    ClienteUpdatedEvent,
    ClienteDeletedEvent,
)
from app.application.validators.cliente import ClienteValidator
from app.domain.repositories.cliente import ClienteRepository


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
        return await self.cliente_repository.get_all()

    async def get_cliente_by_id(self, id: str) -> ClienteEntity | None:
        return await self.cliente_repository.get_by_id(id)

    async def get_cliente_by_cpf(self, cpf: str) -> ClienteEntity | None:
        return await self.cliente_repository.get_by_cpf(cpf)

    async def create_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        ClienteValidator.validate_nome(cliente.nome)
        ClienteValidator.validate_email(cliente.email)
        ClienteValidator.validate_cpf(cliente.cpf)
        ClienteValidator.validate_phone(cliente.telefone)

        created_cliente = await self.cliente_repository.add(cliente)
        self.cliente_created_event.send(created_cliente)
        return created_cliente

    async def update_cliente(self, cliente: ClienteEntity) -> ClienteEntity:
        ClienteValidator.validate_nome(cliente.nome)
        ClienteValidator.validate_email(cliente.email)
        ClienteValidator.validate_cpf(cliente.cpf)
        ClienteValidator.validate_phone(cliente.telefone)

        updated_cliente = await self.cliente_repository.update(cliente)
        self.cliente_updated_event.send(updated_cliente)
        return updated_cliente

    async def delete_cliente(self, id: str) -> bool:
        result = await self.cliente_repository.delete(id)
        if result:
            self.cliente_deleted_event.send(id)
        return result
