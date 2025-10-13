from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.entities.ordem_servico_servico import OrdemServicoServicoEntity, OrdemServicoServicoEntityFactory
from app.domain.entities.ordem_servico_inventory_item import OrdemServicoInventoryItemEntity, OrdemServicoInventoryItemEntityFactory
from app.domain.use_cases.ordem_servico import OrdemServicoUseCases
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.use_cases.servico import ServicoUseCases
from app.domain.repositories.ordem_servico_servico import OrdemServicoServicoRepository
from app.domain.repositories.ordem_servico_inventory_item import OrdemServicoInventoryItemRepository
from app.application.validators.cliente import ClienteValidator
from app.application.validators.servico import ServicoValidator
from app.application.validators.ordem_servico import OrdemServicoValidator
from app.application.validators.veiculo import VeiculoValidator
from app.infrastructure.schemas.ordem_servico import OrdemServicoUpdate
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from datetime import datetime
from typing import Optional
from decimal import Decimal


class OrdemServicoService:
    def __init__(
        self,
        use_case: OrdemServicoUseCases,
        cliente_validator: ClienteValidator,
        vehicle_validator: VeiculoValidator,
        servico_validator: ServicoValidator,
        ordem_servico_validator: OrdemServicoValidator,
        servico_use_case: ServicoUseCases,
        inventory_item_use_case: InventoryItemUseCase,
        os_servico_repository: OrdemServicoServicoRepository,
        os_item_repository: OrdemServicoInventoryItemRepository,
    ):
        self.use_case = use_case
        self.cliente_validator = cliente_validator
        self.vehicle_validator = vehicle_validator
        self.servico_validator = servico_validator
        self.validator = ordem_servico_validator
        self.servico_use_case = servico_use_case
        self.inventory_item_use_case = inventory_item_use_case
        self.os_servico_repository = os_servico_repository
        self.os_item_repository = os_item_repository

    async def criar_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        await self.cliente_validator.validate_exists(ordem_servico.cliente_id)
        await self.vehicle_validator.validate_exists(ordem_servico.vehicle_id)
        for servico_id in ordem_servico.servico_ids:
            await self.servico_validator.validate_exists(servico_id)

        return await self.use_case.create_ordem_servico(ordem_servico)

    async def listar_ordens_servico(self) -> list[OrdemServicoEntity]:
        os_list = await self.use_case.get_all_ordens_servico()
        
        # Filtrar OS finalizadas ou canceladas (exclusão lógica)
        os_list = [
            os for os in os_list 
            if os.status not in (StatusOrdemServico.FINALIZADA, StatusOrdemServico.CANCELADA)
        ]

        # Definir prioridade de ordenação por status
        status_priority = {
            StatusOrdemServico.EM_EXECUCAO: 1,
            StatusOrdemServico.AGUARDANDO_APROVACAO: 2,
            StatusOrdemServico.EM_DIAGNOSTICO: 3,
            StatusOrdemServico.RECEBIDA: 4
        }

        # Ordenar primeiro pelo status (prioridade), depois pela data mais antiga
        os_list.sort(
            key=lambda os: (status_priority.get(os.status, 99), os.data_abertura)
        )

        return os_list

    async def buscar_ordem_servico_por_id(self, id: str) -> OrdemServicoEntity | None:
        return await self.use_case.get_ordem_servico_by_id(id)

    async def listar_ordens_servico_por_status(self, status: StatusOrdemServico) -> list[OrdemServicoEntity]:
        return await self.use_case.get_ordens_servico_by_status(status)

    async def atualizar_ordem_servico(
        self, id: str, dados: OrdemServicoUpdate
    ) -> OrdemServicoEntity:
        os = await self.use_case.get_ordem_servico_by_id(id)
        if not os:
            raise ValueError("Ordem de serviço não encontrada")

        # Atualiza apenas os campos recebidos
        if dados.status is not None:
            self.validator.validate_status_transition(os.status, dados.status)
            os.status = dados.status
        if dados.mecanico_id is not None:
            os.mecanico_id = dados.mecanico_id
        if dados.orcamento_id is not None:
            os.orcamento_id = dados.orcamento_id
        if dados.data_fechamento is not None:
            os.data_fechamento = dados.data_fechamento

        return await self.use_case.update_ordem_servico(os)

    async def finalizar(self, id: str) -> OrdemServicoEntity:
        return await self._atualizar_status(
            id, StatusOrdemServico.FINALIZADA, fechar=True
        )

    async def cancelar(self, id: str) -> OrdemServicoEntity:
        return await self._atualizar_status(
            id, StatusOrdemServico.CANCELADA, fechar=True
        )

    async def iniciar_execucao(self, id: str) -> OrdemServicoEntity:
        return await self._atualizar_status(id, StatusOrdemServico.EM_EXECUCAO)

    async def _atualizar_status(
        self, id: str, novo_status: StatusOrdemServico, fechar: bool = False
    ) -> OrdemServicoEntity:
        os = await self.use_case.get_ordem_servico_by_id(id)
        if not os:
            raise ValueError("Ordem de serviço não encontrada")

        self.validator.validate_status_transition(os.status, novo_status)
        os.status = novo_status

        if fechar:
            os.data_fechamento = os.data_fechamento or datetime.utcnow()

        return await self.use_case.update_ordem_servico(os)

    async def adicionar_servico(
        self, ordem_servico_id: str, servico_id: str, observacoes: Optional[str] = None
    ) -> OrdemServicoServicoEntity:
        """Adiciona um serviço a uma ordem de serviço, copiando automaticamente o valor atual do serviço"""
        
        # Verificar se a OS existe
        os = await self.use_case.get_ordem_servico_by_id(ordem_servico_id)
        if not os:
            raise ValueError("Ordem de serviço não encontrada")
        
        # Verificar se o serviço existe e buscar o preço atual
        servico = await self.servico_use_case.get_servico_by_id(servico_id)
        if not servico:
            raise ValueError("Serviço não encontrado")
        
        # Criar a entidade de relação com o valor atual do serviço
        relacao = OrdemServicoServicoEntityFactory.create(
            id=None,
            ordem_servico_id=ordem_servico_id,
            servico_id=servico_id,
            valor_servico=Decimal(str(servico.preco)),
            observacoes=observacoes
        )
        
        return await self.os_servico_repository.adicionar_servico_a_os(relacao)
    
    async def adicionar_item_inventario(
        self, ordem_servico_id: str, inventory_item_id: int, quantidade: int
    ) -> OrdemServicoInventoryItemEntity:
        """Adiciona um item de inventário a uma ordem de serviço, copiando automaticamente o valor atual do item"""
        
        # Verificar se a OS existe
        os = await self.use_case.get_ordem_servico_by_id(ordem_servico_id)
        if not os:
            raise ValueError("Ordem de serviço não encontrada")
        
        # Verificar se o item existe e buscar o preço atual
        item = await self.inventory_item_use_case.get_item(inventory_item_id)
        if not item:
            raise ValueError("Item de inventário não encontrado")
        
        # Verificar se há estoque suficiente
        if item.quantity < quantidade:
            raise ValueError(f"Estoque insuficiente. Disponível: {item.quantity}, Solicitado: {quantidade}")
        
        # Criar a entidade de relação com o valor atual do item
        relacao = OrdemServicoInventoryItemEntityFactory.create(
            id=None,
            ordem_servico_id=ordem_servico_id,
            inventory_item_id=inventory_item_id,
            quantidade=quantidade,
            valor_unitario=Decimal(str(item.unit_price))
        )
        
        return await self.os_item_repository.adicionar_item_a_os(relacao)

    async def aprovar_orcamento(self, ordem_servico_id: str) -> OrdemServicoEntity:
        """Aprova o orçamento e move a OS para execução."""
        os_entity = await self.use_case.get_ordem_servico_by_id(ordem_servico_id)
        if not os_entity:
            raise ValueError("Ordem de serviço não encontrada")

        # Verifica se está no status correto
        if os_entity.status != StatusOrdemServico.AGUARDANDO_APROVACAO:
            raise ValueError(
                f"A OS precisa estar em 'aguardando_aprovacao' para ser aprovada "
                f"(atual: {os_entity.status})."
            )

        # Valida transição de status
        self.validator.validate_status_transition(
            os_entity.status, StatusOrdemServico.EM_EXECUCAO
        )

        # Atualiza status
        os_entity.status = StatusOrdemServico.EM_EXECUCAO

        # Persiste a atualização
        return await self.use_case.update_ordem_servico(os_entity)


    async def recusar_orcamento(self, ordem_servico_id: str) -> OrdemServicoEntity:
        os_entity = await self.use_case.get_ordem_servico_by_id(ordem_servico_id)
        if not os_entity:
            raise ValueError("Ordem de serviço não encontrada")

        if os_entity.status != StatusOrdemServico.AGUARDANDO_APROVACAO:
            raise ValueError(
                f"A OS precisa estar em 'aguardando_aprovacao' para ser recusada (atual: {os_entity.status})."
            )

        os_entity.status = StatusOrdemServico.CANCELADA
        if hasattr(os_entity, "motivo_cancelamento"):
            os_entity.motivo_cancelamento = "Orçamento recusado pelo cliente"

        updated = await self.use_case.update_ordem_servico(os_entity)
        return updated
