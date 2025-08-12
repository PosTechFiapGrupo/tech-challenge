from decimal import Decimal
from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.ordem_servico_servico import (
    OrdemServicoServicoEntity,
)
from app.domain.repositories.ordem_servico_servico import OrdemServicoServicoRepository
from app.infrastructure.models.ordem_servico_servico import OrdemServicoServicoModel
from app.infrastructure.models.ordem_servico import OrdemServicoModel
from app.infrastructure.database import database
from datetime import timedelta
from sqlalchemy import select, func, text

class OrdemServicoServicoRepositoryImpl(OrdemServicoServicoRepository):
    def __init__(self):
        self.database = database

    async def adicionar_servico_a_os(
        self, os_servico: OrdemServicoServicoEntity
    ) -> OrdemServicoServicoEntity:
        async for session in self.database.get_session():
            model = OrdemServicoServicoModel(
                ordem_servico_id=os_servico.ordem_servico_id,
                servico_id=os_servico.servico_id,
                valor_servico=os_servico.valor_servico,
                observacoes=os_servico.observacoes,
            )
            
            session.add(model)
            await session.flush()
            await session.commit()
            
            # Retorna a entidade com o ID gerado
            return OrdemServicoServicoEntity(
                id=model.id,
                ordem_servico_id=model.ordem_servico_id,
                servico_id=model.servico_id,
                valor_servico=Decimal(str(model.valor_servico)),
                observacoes=model.observacoes,
            )

    async def listar_servicos_por_os(self, ordem_servico_id: str) -> List[OrdemServicoServicoEntity]:
        async for session in self.database.get_session():
            stmt = select(OrdemServicoServicoModel).where(
                OrdemServicoServicoModel.ordem_servico_id == ordem_servico_id
            )
            result = await session.execute(stmt)
            models = result.scalars().all()
            
            return [
                OrdemServicoServicoEntity(
                    id=model.id,
                    ordem_servico_id=model.ordem_servico_id,
                    servico_id=model.servico_id,
                    valor_servico=Decimal(str(model.valor_servico)),
                    observacoes=model.observacoes,
                )
                for model in models
            ]

    async def remover_servico_da_os(self, ordem_servico_id: str, servico_id: int) -> bool:
        async for session in self.database.get_session():
            stmt = delete(OrdemServicoServicoModel).where(
                OrdemServicoServicoModel.ordem_servico_id == ordem_servico_id,
                OrdemServicoServicoModel.servico_id == servico_id,
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    async def calcular_tempo_medio_execucao(self) -> timedelta | None:
        async for session in self.database.get_session():
            query = select(
                func.avg(
                    func.timestampdiff(
                        text('SECOND'),
                        OrdemServicoModel.data_abertura,
                        OrdemServicoModel.data_fechamento
                    )
                )
            ).where(OrdemServicoModel.data_fechamento.isnot(None))

            result = await session.execute(query)
            tempo_medio_segundos = result.scalar()
            if tempo_medio_segundos is not None:
                return timedelta(seconds=float(tempo_medio_segundos))  # CONVERTE PARA float AQUI
            return None