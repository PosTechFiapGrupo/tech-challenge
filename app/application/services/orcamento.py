from decimal import Decimal
from typing import List
from app.domain.repositories.ordem_servico import OrdemServicoRepository
from app.domain.repositories.servico import ServicoRepository
from app.domain.repositories.inventory_item_repository import InventoryItemRepository
from app.domain.repositories.ordem_servico_servico import OrdemServicoServicoRepository
from app.domain.repositories.ordem_servico_inventory_item import OrdemServicoInventoryItemRepository
from app.infrastructure.schemas.orcamento import OrcamentoOutput, ServicoOrcamento, InventoryItemOrcamento
from app.infrastructure.schemas.servico import ServicoOutput
from app.infrastructure.schemas.inventory_item_schema import InventoryItemOut
from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput


class OrcamentoService:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepository,
        servico_repository: ServicoRepository,
        inventory_repository: InventoryItemRepository,
        os_servico_repository: OrdemServicoServicoRepository,
        os_inventory_repository: OrdemServicoInventoryItemRepository,
    ):
        self.ordem_servico_repository = ordem_servico_repository
        self.servico_repository = servico_repository
        self.inventory_repository = inventory_repository
        self.os_servico_repository = os_servico_repository
        self.os_inventory_repository = os_inventory_repository

    async def gerar_orcamento(self, ordem_servico_id: str) -> OrcamentoOutput:
        # Buscar a ordem de serviço
        os_entity = await self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not os_entity:
            raise ValueError("Ordem de serviço não encontrada")

        # Buscar serviços da OS
        servicos_os = await self.os_servico_repository.listar_servicos_por_os(ordem_servico_id)
        servicos_orcamento = []
        total_servicos = Decimal("0.00")

        for servico_os in servicos_os:
            servico_entity = await self.servico_repository.get_by_id(servico_os.servico_id)
            if servico_entity:
                servico_output = ServicoOutput(
                    id=servico_entity.id,
                    descricao=servico_entity.descricao,
                    preco=servico_entity.preco
                )
                
                servico_orcamento = ServicoOrcamento(
                    servico=servico_output,
                    valor_na_os=servico_os.valor_servico,
                    observacoes=servico_os.observacoes
                )
                servicos_orcamento.append(servico_orcamento)
                total_servicos += servico_os.valor_servico

        # Buscar itens de inventário da OS
        itens_os = await self.os_inventory_repository.listar_itens_por_os(ordem_servico_id)
        itens_orcamento = []
        total_items = Decimal("0.00")

        for item_os in itens_os:
            item_entity = await self.inventory_repository.get_by_id(item_os.inventory_item_id)
            if item_entity:
                item_output = InventoryItemOut(
                    id=item_entity.id or 0,
                    name=item_entity.name,
                    description=item_entity.description,
                    quantity=item_entity.quantity,
                    minimum_stock=item_entity.minimum_stock,
                    unit_price=item_entity.unit_price
                )
                
                valor_total_item = item_os.quantidade * item_os.valor_unitario
                
                item_orcamento = InventoryItemOrcamento(
                    item=item_output,
                    quantidade=item_os.quantidade,
                    valor_unitario_na_os=item_os.valor_unitario,
                    valor_total=valor_total_item
                )
                itens_orcamento.append(item_orcamento)
                total_items += valor_total_item

        # Converter entidade da OS para output
        os_output = OrdemServicoOutput(
            id=os_entity.id,
            cliente_id=os_entity.cliente_id,
            vehicle_id=os_entity.vehicle_id,
            servico_ids=os_entity.servico_ids,
            mecanico_id=os_entity.mecanico_id,
            atendente_id=os_entity.atendente_id,
            orcamento_id=os_entity.orcamento_id,
            status=os_entity.status,
            data_abertura=os_entity.data_abertura,
            data_fechamento=os_entity.data_fechamento
        )

        # Calcular total geral
        total_geral = total_servicos + total_items

        return OrcamentoOutput(
            ordem_servico=os_output,
            servicos=servicos_orcamento,
            inventory_items=itens_orcamento,
            total_servicos=total_servicos,
            total_items=total_items,
            total_geral=total_geral
        )
