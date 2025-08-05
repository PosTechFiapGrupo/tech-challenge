from app.domain.events.servico import (
    ServicoCreatedEvent,
    ServicoUpdatedEvent,
    ServicoDeletedEvent,
)
from app.domain.entities.servico import ServicoEntity


class ServicoCreatedQueueEvent(ServicoCreatedEvent):

    def send(self, servico: ServicoEntity) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        # Por exemplo, RabbitMQ, Redis, etc.
        print(f"Serviço criado: {servico.descricao} (ID: {servico.id})")
        return True


class ServicoUpdatedQueueEvent(ServicoUpdatedEvent):

    def send(self, servico: ServicoEntity) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        print(f"Serviço atualizado: {servico.descricao} (ID: {servico.id})")
        return True


class ServicoDeletedQueueEvent(ServicoDeletedEvent):

    def send(self, servico_id: str) -> bool:
        # Aqui você pode implementar a lógica para enviar o evento para uma fila
        print(f"Serviço deletado (ID: {servico_id})")
        return True
