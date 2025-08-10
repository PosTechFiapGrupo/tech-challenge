from sqlalchemy.future import select
from app.domain.entities.ordem_servico import OrdemServicoEntity, OrdemServicoEntityFactory
from app.domain.repositories.ordem_servico import OrdemServicoRepository
from app.infrastructure.models.ordem_servico import OrdemServicoModel
from app.infrastructure.models.ordem_servico_servico import OrdemServicoServicoModel
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from app.infrastructure.database import database


class OrdemServicoRepositoryImpl(OrdemServicoRepository):
    def __init__(self):
        self.database = database

    async def _get_servico_ids_for_ordem(self, session, ordem_servico_id: str) -> list[str]:
        """Busca os IDs dos serviços associados a uma ordem de serviço"""
        result = await session.execute(
            select(OrdemServicoServicoModel.servico_id)
            .where(OrdemServicoServicoModel.ordem_servico_id == ordem_servico_id)
        )
        return [str(servico_id) for servico_id in result.scalars().all()]

    async def create(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        async for session in self.database.get_session():
            # Criar o modelo da ordem de serviço
            model = OrdemServicoModel(
                id=ordem_servico.id,
                cliente_id=ordem_servico.cliente_id,
                vehicle_id=ordem_servico.vehicle_id,
                mecanico_id=ordem_servico.mecanico_id,
                atendente_id=ordem_servico.atendente_id,
                orcamento_id=ordem_servico.orcamento_id,
                status=ordem_servico.status.value,
                data_abertura=ordem_servico.data_abertura,
                data_fechamento=ordem_servico.data_fechamento,
            )

            session.add(model)
            await session.flush()  # Para obter o ID gerado

            # Criar os relacionamentos com serviços na tabela separada
            for servico_id in ordem_servico.servico_ids:
                relacao = OrdemServicoServicoModel(
                    ordem_servico_id=str(model.id),
                    servico_id=servico_id,
                    observacoes=None  # Pode ser definido posteriormente
                )
                session.add(relacao)

            await session.commit()
            
            # Buscar os servico_ids para retornar
            servico_ids = await self._get_servico_ids_for_ordem(session, str(model.id))
            
            return OrdemServicoEntityFactory.create(
                id=str(model.id),
                cliente_id=str(model.cliente_id),
                vehicle_id=model.vehicle_id,
                servico_ids=servico_ids,
                mecanico_id=str(model.mecanico_id) if model.mecanico_id else None,
                atendente_id=str(model.atendente_id) if model.atendente_id else None,
                orcamento_id=str(model.orcamento_id) if model.orcamento_id else None,
                status=StatusOrdemServico(model.status),
                data_abertura=model.data_abertura,
            )

    async def get_by_id(self, id: str) -> OrdemServicoEntity | None:
        async for session in self.database.get_session():
            result = await session.execute(
                select(OrdemServicoModel)
                .where(OrdemServicoModel.id == id)
            )
            model = result.scalar_one_or_none()
            if not model:
                return None
            
            # Buscar os servico_ids
            servico_ids = await self._get_servico_ids_for_ordem(session, str(model.id))
            
            return OrdemServicoEntityFactory.create(
                id=str(model.id),
                cliente_id=str(model.cliente_id),
                vehicle_id=model.vehicle_id,
                servico_ids=servico_ids,
                mecanico_id=str(model.mecanico_id) if model.mecanico_id else None,
                atendente_id=str(model.atendente_id) if model.atendente_id else None,
                orcamento_id=str(model.orcamento_id) if model.orcamento_id else None,
                status=StatusOrdemServico(model.status),
                data_abertura=model.data_abertura,
            )

    async def get_all(self) -> list[OrdemServicoEntity]:
        async for session in self.database.get_session():
            result = await session.execute(select(OrdemServicoModel))
            models = result.scalars().all()
            entities = []
            for model in models:
                # Buscar os servico_ids para cada modelo
                servico_ids = await self._get_servico_ids_for_ordem(session, str(model.id))
                
                entity = OrdemServicoEntityFactory.create(
                    id=str(model.id),
                    cliente_id=str(model.cliente_id),
                    vehicle_id=model.vehicle_id,
                    servico_ids=servico_ids,
                    mecanico_id=str(model.mecanico_id) if model.mecanico_id else None,
                    atendente_id=str(model.atendente_id) if model.atendente_id else None,
                    orcamento_id=str(model.orcamento_id) if model.orcamento_id else None,
                    status=StatusOrdemServico(model.status),
                    data_abertura=model.data_abertura,
                )
                entities.append(entity)
            return entities

    async def update(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        async for session in self.database.get_session():
            model = await session.get(OrdemServicoModel, ordem_servico.id)
            if not model:
                raise ValueError("Ordem de serviço não encontrada")

            # Atualizar os campos
            model.status = ordem_servico.status.value
            model.mecanico_id = ordem_servico.mecanico_id
            model.orcamento_id = ordem_servico.orcamento_id
            model.data_fechamento = ordem_servico.data_fechamento

            await session.commit()
            
            # Buscar os servico_ids para retornar
            servico_ids = await self._get_servico_ids_for_ordem(session, str(model.id))
            
            return OrdemServicoEntityFactory.create(
                id=str(model.id),
                cliente_id=str(model.cliente_id),
                vehicle_id=model.vehicle_id,
                servico_ids=servico_ids,
                mecanico_id=str(model.mecanico_id) if model.mecanico_id else None,
                atendente_id=str(model.atendente_id) if model.atendente_id else None,
                orcamento_id=str(model.orcamento_id) if model.orcamento_id else None,
                status=StatusOrdemServico(model.status),
                data_abertura=model.data_abertura,
            )
