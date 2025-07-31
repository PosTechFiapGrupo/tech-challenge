from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.cliente import ClienteEntity, ClienteEntityFactory
from app.domain.repositories.cliente import ClienteRepository
from app.infrastructure.models.cliente import ClienteModel
from app.infrastructure.database import database


class ClienteRepositoryImpl(ClienteRepository):
    
    def __init__(self):
        self.database = database

    async def get_all(self) -> list[ClienteEntity]:
        async for session in self.database.get_session():
            stmt = select(ClienteModel)
            result = await session.execute(stmt)
            clientes = result.scalars().all()
            
            return [
                ClienteEntityFactory.create(
                    id=str(cliente.id),
                    nome=cliente.nome,
                    telefone=cliente.telefone,
                    email=cliente.email,
                    cpf=cliente.cpf
                ) 
                for cliente in clientes
            ]

    async def get_by_id(self, id: str) -> ClienteEntity | None:
        try:
            cliente_id = int(id)
        except ValueError:
            return None
            
        async for session in self.database.get_session():
            stmt = select(ClienteModel).where(ClienteModel.id == cliente_id)
            result = await session.execute(stmt)
            cliente = result.scalar_one_or_none()
            
            if cliente is None:
                return None
                
            return ClienteEntityFactory.create(
                id=str(cliente.id),
                nome=cliente.nome,
                telefone=cliente.telefone,
                email=cliente.email,
                cpf=cliente.cpf
            )

    async def get_by_cpf(self, cpf: str) -> ClienteEntity | None:
        cpf_clean = cpf.replace('.', '').replace('-', '').strip()
        
        async for session in self.database.get_session():
            stmt = select(ClienteModel).where(
                (ClienteModel.cpf == cpf) | 
                (ClienteModel.cpf == cpf_clean)
            )
            result = await session.execute(stmt)
            cliente = result.scalar_one_or_none()
            
            if cliente is None:
                return None
                
            return ClienteEntityFactory.create(
                id=str(cliente.id),
                nome=cliente.nome,
                telefone=cliente.telefone,
                email=cliente.email,
                cpf=cliente.cpf
            )

    async def add(self, cliente: ClienteEntity) -> ClienteEntity:
        async for session in self.database.get_session():
            cliente_model = ClienteModel(
                nome=cliente.nome,
                telefone=cliente.telefone,
                email=cliente.email,
                cpf=cliente.cpf
            )
            session.add(cliente_model)
            await session.flush()
            await session.refresh(cliente_model)
            await session.commit()  # Commit explícito
            
            cliente.id = str(cliente_model.id)
            return cliente

    async def update(self, cliente: ClienteEntity) -> ClienteEntity:
        try:
            cliente_id = int(cliente.id)
        except ValueError:
            raise ValueError(f"Invalid cliente ID: {cliente.id}")
            
        async for session in self.database.get_session():
            stmt = update(ClienteModel).where(ClienteModel.id == cliente_id).values(
                nome=cliente.nome,
                telefone=cliente.telefone,
                email=cliente.email,
                cpf=cliente.cpf
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise ValueError(f"Cliente with id {cliente.id} not found")
            
            await session.commit()  # Commit explícito
            return cliente

    async def delete(self, id: str) -> bool:
        try:
            cliente_id = int(id)
        except ValueError:
            return False
            
        async for session in self.database.get_session():
            stmt = delete(ClienteModel).where(ClienteModel.id == cliente_id)
            result = await session.execute(stmt)
            success = result.rowcount > 0
            if success:
                await session.commit()  # Commit explícito
            return success
