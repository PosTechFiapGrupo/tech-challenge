from app.domain.events.user_event import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent,
)
from app.domain.entities.user import UserEntity


class UserCreatedQueueEvent(UserCreatedEvent):

    def send(self, user: UserEntity) -> bool:
        # Implemente aqui a lógica para enviar o evento para uma fila (RabbitMQ, Redis, etc.)
        print(f"Usuário criado: {user.nome} (ID: {user.id})")
        return True


class UserUpdatedQueueEvent(UserUpdatedEvent):

    def send(self, user: UserEntity) -> bool:
        # Implemente aqui a lógica para enviar o evento para uma fila
        print(f"Usuário atualizado: {user.nome} (ID: {user.id})")
        return True


class UserDeletedQueueEvent(UserDeletedEvent):

    def send(self, user_id: int) -> bool:
        # Implemente aqui a lógica para enviar o evento para uma fila
        print(f"Usuário deletado (ID: {user_id})")
        return True
