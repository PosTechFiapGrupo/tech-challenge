from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.repositories.ordem_servico import OrdemServicoRepository
from app.infrastructure.models.ordem_servico import OrdemServicoModel
from app.infrastructure.models.servico import ServicoModel
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from enum import Enum
from app.infrastructure.database import database


class OrdemServicoRepositoryImpl(OrdemServicoRepository):
    def __init__(self):
        self.database = database

    @staticmethod
    def _model_to_entity(model: OrdemServicoModel) -> OrdemServicoEntity:
        return OrdemServicoEntity(
            uid=str(model.id),
            cliente_id=str(model.cliente_id),
            vehicle_id=model.vehicle_id,
            mecanico_id=str(model.mecanico_id) if model.mecanico_id else None,
            atendente_id=str(model.atendente_id) if model.atendente_id else None,
            orcamento_id=str(model.orcamento_id) if model.orcamento_id else None,
            status=StatusOrdemServico(model.status),
            data_abertura=model.data_abertura,
            data_fechamento=model.data_fechamento,
            servico_ids=[str(s.id) for s in model.servicos],
        )

    async def create(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            servicos = await session.execute(
                select(ServicoModel).where(
                    ServicoModel.id.in_([int(sid) for sid in ordem_servico.servico_ids])
                )
            )
            servico_models = servicos.scalars().all()

            model = OrdemServicoModel(
                cliente_id=int(ordem_servico.cliente_id),
                vehicle_id=int(ordem_servico.vehicle_id),
                mecanico_id=(
                    int(ordem_servico.mecanico_id)
                    if ordem_servico.mecanico_id
                    else None
                ),
                atendente_id=(
                    int(ordem_servico.atendente_id)
                    if ordem_servico.atendente_id
                    else None
                ),
                orcamento_id=(
                    int(ordem_servico.orcamento_id)
                    if ordem_servico.orcamento_id
                    else None
                ),
                status=(
                    ordem_servico.status.value
                    if isinstance(ordem_servico.status, Enum)
                    else ordem_servico.status
                ),
                data_abertura=ordem_servico.data_abertura,
                data_fechamento=ordem_servico.data_fechamento,
            )

            model.servicos = servico_models

            session.add(model)
            await session.flush()
            await session.commit()

            return self._model_to_entity(model)

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()

    async def get_by_id(self, id: int) -> OrdemServicoEntity | None:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            result = await session.execute(
                select(OrdemServicoModel)
                .options(selectinload(OrdemServicoModel.servicos))
                .where(OrdemServicoModel.id == id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_entity(model) if model else None

        finally:
            await session.close()

    async def get_all(self) -> list[OrdemServicoEntity]:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            result = await session.execute(
                select(OrdemServicoModel).options(
                    selectinload(OrdemServicoModel.servicos)
                )
            )
            models = result.scalars().all()
            return [self._model_to_entity(m) for m in models]

        finally:
            await session.close()

    async def update(self, ordem_servico: OrdemServicoEntity) -> OrdemServicoEntity:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            model = await session.get(OrdemServicoModel, int(ordem_servico.id))
            if not model:
                raise ValueError("Ordem de serviço não encontrada")

            model.status = ordem_servico.status.value
            model.mecanico_id = (
                int(ordem_servico.mecanico_id) if ordem_servico.mecanico_id else None
            )
            model.orcamento_id = (
                int(ordem_servico.orcamento_id) if ordem_servico.orcamento_id else None
            )
            model.data_fechamento = ordem_servico.data_fechamento

            await session.flush()
            await session.commit()
            return self._model_to_entity(model)

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()
