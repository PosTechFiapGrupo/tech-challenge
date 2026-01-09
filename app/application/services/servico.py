from typing import List

from app.application.validators.servico import ServicoValidator
from app.domain.entities.servico import ServicoEntity
from app.domain.events.servico import (
    ServicoCreatedEvent,
    ServicoDeletedEvent,
    ServicoUpdatedEvent,
)
from app.domain.repositories.servico import ServicoRepository
from app.domain.use_cases.servico import ServicoUseCases
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class ServicoService(ServicoUseCases):

    def __init__(
        self,
        servico_repository: ServicoRepository,
        servico_created_event: ServicoCreatedEvent,
        servico_updated_event: ServicoUpdatedEvent,
        servico_deleted_event: ServicoDeletedEvent,
    ):
        super().__init__(
            servico_repository,
            servico_created_event,
            servico_updated_event,
            servico_deleted_event,
        )

    async def get_all_servicos(self) -> List[ServicoEntity]:
        servicos = await self.servico_repository.get_all()
        logger.info("Serviços listados", extra={"count": len(servicos)})
        return servicos

    async def get_servico_by_id(self, id: str) -> ServicoEntity | None:
        servico = await self.servico_repository.get_by_id(id)
        logger.info("Serviço buscado por ID", extra={"servico_id": id, "found": servico is not None})
        return servico

    async def create_servico(self, servico: ServicoEntity) -> ServicoEntity:
        ServicoValidator.validate_descricao(servico.descricao)
        ServicoValidator.validate_preco(servico.preco)

        created_servico = await self.servico_repository.add(servico)
        self.servico_created_event.send(created_servico)
        logger.info("Serviço criado", extra={"servico_id": str(created_servico.id), "descricao": servico.descricao})
        return created_servico

    async def update_servico(self, servico: ServicoEntity) -> ServicoEntity:
        ServicoValidator.validate_descricao(servico.descricao)
        ServicoValidator.validate_preco(servico.preco)

        updated_servico = await self.servico_repository.update(servico)
        self.servico_updated_event.send(updated_servico)
        logger.info("Serviço atualizado", extra={"servico_id": str(servico.id)})
        return updated_servico

    async def delete_servico(self, id: str) -> bool:
        result = await self.servico_repository.delete(id)
        if result:
            self.servico_deleted_event.send(id)
            logger.info("Serviço deletado", extra={"servico_id": id})
        else:
            logger.warning("Falha ao deletar serviço", extra={"servico_id": id})
        return result
