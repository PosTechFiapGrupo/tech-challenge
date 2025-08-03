from app.domain.events.cliente import (
    ClienteCreatedEvent,
    ClienteUpdatedEvent,
    ClienteDeletedEvent,
)
from app.domain.entities.cliente import ClienteEntity


class ClienteCreatedQueueEvent(ClienteCreatedEvent):

    def send(self, cliente: ClienteEntity) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        # Por exemplo, RabbitMQ, Redis, etc.
        print(f"Cliente criado: {cliente.nome} (ID: {cliente.id})")
        return True


class ClienteUpdatedQueueEvent(ClienteUpdatedEvent):

    def send(self, cliente: ClienteEntity) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        print(f"Cliente atualizado: {cliente.nome} (ID: {cliente.id})")
        return True


class ClienteDeletedQueueEvent(ClienteDeletedEvent):

    def send(self, cliente_id: str) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        print(f"Cliente deletado (ID: {cliente_id})")
        return True
