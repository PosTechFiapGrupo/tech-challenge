from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.use_cases.ordem_servico import OrdemServicoUseCases
from app.application.validators.cliente import ClienteValidator
from app.application.validators.servico import ServicoValidator
from app.application.validators.ordem_servico import OrdemServicoValidator
from app.infrastructure.schemas.ordem_servico import OrdemServicoUpdate
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from datetime import datetime


class OrdemServicoService:
    def __init__(
        self,
        use_case: OrdemServicoUseCases,
        cliente_validator: ClienteValidator,
        # veiculo_validator: VeiculoValidator,
        servico_validator: ServicoValidator,
        ordem_servico_validator: OrdemServicoValidator,
    ):
        self.use_case = use_case
        self.cliente_validator = cliente_validator
        # self.veiculo_validator = veiculo_validator
        self.servico_validator = servico_validator
        self.validator = ordem_servico_validator

    async def criar_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        await self.cliente_validator.validate_exists(ordem_servico.cliente_id)
        for servico_id in ordem_servico.servico_ids:
            await self.servico_validator.validate_exists(servico_id)

        return await self.use_case.create_ordem_servico(ordem_servico)

    async def listar_ordens_servico(self) -> list[OrdemServicoEntity]:
        return await self.use_case.get_all_ordens_servico()

    async def buscar_ordem_servico_por_id(self, id: str) -> OrdemServicoEntity | None:
        return await self.use_case.get_ordem_servico_by_id(id)

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
