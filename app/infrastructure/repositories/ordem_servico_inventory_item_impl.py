from decimal import Decimal
from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.ordem_servico_inventory_item import (
    OrdemServicoInventoryItemEntity,
)
from app.domain.repositories.ordem_servico_inventory_item import OrdemServicoInventoryItemRepository
from app.infrastructure.models.ordem_servico_inventory_item import OrdemServicoInventoryItemModel
from app.infrastructure.database import database


class OrdemServicoInventoryItemRepositoryImpl(OrdemServicoInventoryItemRepository):
    def __init__(self):
        self.database = database

    async def adicionar_item_a_os(
        self, os_item: OrdemServicoInventoryItemEntity
    ) -> OrdemServicoInventoryItemEntity:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            model = OrdemServicoInventoryItemModel(
                ordem_servico_id=os_item.ordem_servico_id,
                inventory_item_id=os_item.inventory_item_id,
                quantidade=os_item.quantidade,
                valor_unitario=os_item.valor_unitario,
            )
            
            session.add(model)
            await session.flush()
            await session.commit()
            
            # Retorna a entidade com o ID gerado
            return OrdemServicoInventoryItemEntity(
                id=model.id,
                ordem_servico_id=model.ordem_servico_id,
                inventory_item_id=model.inventory_item_id,
                quantidade=model.quantidade,
                valor_unitario=Decimal(str(model.valor_unitario)),
            )

        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def listar_itens_por_os(self, ordem_servico_id: str) -> List[OrdemServicoInventoryItemEntity]:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            stmt = select(OrdemServicoInventoryItemModel).where(
                OrdemServicoInventoryItemModel.ordem_servico_id == ordem_servico_id
            )
            result = await session.execute(stmt)
            models = result.scalars().all()
            
            return [
                OrdemServicoInventoryItemEntity(
                    id=model.id,
                    ordem_servico_id=model.ordem_servico_id,
                    inventory_item_id=model.inventory_item_id,
                    quantidade=model.quantidade,
                    valor_unitario=Decimal(str(model.valor_unitario)),
                )
                for model in models
            ]
        finally:
            await session.close()

    async def remover_item_da_os(self, ordem_servico_id: str, inventory_item_id: int) -> bool:
        session_gen = self.database.get_session()
        session = await session_gen.__anext__()
        try:
            stmt = delete(OrdemServicoInventoryItemModel).where(
                OrdemServicoInventoryItemModel.ordem_servico_id == ordem_servico_id,
                OrdemServicoInventoryItemModel.inventory_item_id == inventory_item_id,
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
