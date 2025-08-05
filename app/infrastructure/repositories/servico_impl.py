from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.servico import ServicoEntity, ServicoEntityFactory
from app.domain.repositories.servico import ServicoRepository
from app.infrastructure.models.servico import ServicoModel
from app.infrastructure.database import database


class ServicoRepositoryImpl(ServicoRepository):
    
    def __init__(self):
        self.database = database

    async def get_all(self) -> List[ServicoEntity]:
        async for session in self.database.get_session():
            stmt = select(ServicoModel)
            result = await session.execute(stmt)
            servicos = result.scalars().all()
            return [
                ServicoEntityFactory.create(
                    id=str(servico.id),
                    descricao=servico.descricao,
                    preco=float(servico.preco)
                ) 
                for servico in servicos
            ]

    async def get_by_id(self, id: str) -> ServicoEntity | None:
        try:
            servico_id = int(id)
        except ValueError:
            return None
            
        async for session in self.database.get_session():
            stmt = select(ServicoModel).where(ServicoModel.id == servico_id)
            result = await session.execute(stmt)
            servico = result.scalar_one_or_none()
            
            if servico is None:
                return None
                
            return ServicoEntityFactory.create(
                id=str(servico.id),
                descricao=servico.descricao,
                preco=float(servico.preco)
            )

    async def add(self, servico: ServicoEntity) -> ServicoEntity:
        async for session in self.database.get_session():
            servico_model = ServicoModel(
                descricao=servico.descricao,
                preco=servico.preco
            )
            session.add(servico_model)
            await session.flush()
            await session.refresh(servico_model)
            await session.commit()  # Commit explícito
            
            servico.id = str(servico_model.id)
            return servico

    async def update(self, servico: ServicoEntity) -> ServicoEntity:
        try:
            servico_id = int(servico.id)
        except ValueError:
            raise ValueError(f"Invalid servico ID: {servico.id}")
            
        async for session in self.database.get_session():
            stmt = update(ServicoModel).where(ServicoModel.id == servico_id).values(
                descricao=servico.descricao,
                preco=servico.preco
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise ValueError(f"Servico with id {servico.id} not found")
            
            await session.commit()  # Commit explícito
            return servico

    async def delete(self, id: str) -> bool:
        try:
            servico_id = int(id)
        except ValueError:
            return False
            
        async for session in self.database.get_session():
            stmt = delete(ServicoModel).where(ServicoModel.id == servico_id)
            result = await session.execute(stmt)
            success = result.rowcount > 0
            if success:
                await session.commit()  # Commit explícito
            return success
