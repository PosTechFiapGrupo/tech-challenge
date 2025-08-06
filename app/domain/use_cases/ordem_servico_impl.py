from typing import List
from app.domain.entities.ordem_servico import OrdemServicoEntity
from app.domain.use_cases.ordem_servico import OrdemServicoUseCases
from app.domain.repositories.ordem_servico import OrdemServicoRepository
from app.domain.events.ordem_servico import (
    OrdemServicoSolicitadaEvent,
    OrcamentoSolicitadoEvent,
    MecanicoDesignadoEvent,
    ServicosIncluidosEvent,
    PecaOuInsumoIncluidoEvent,
    OrcamentoGeradoEvent,
    OrcamentoEnviadoAoClienteEvent,
    OrdemServicoAceitaEvent,
    OrdemServicoRealizadaEvent,
)
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoUseCasesImpl(OrdemServicoUseCases):
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepository,
        os_criada_event: OrdemServicoSolicitadaEvent,
        orcamento_solicitado_event: OrcamentoSolicitadoEvent,
        mecanico_designado_event: MecanicoDesignadoEvent,
        servicos_incluidos_event: ServicosIncluidosEvent,
        peca_incluida_event: PecaOuInsumoIncluidoEvent,
        orcamento_gerado_event: OrcamentoGeradoEvent,
        orcamento_enviado_event: OrcamentoEnviadoAoClienteEvent,
        os_aceita_event: OrdemServicoAceitaEvent,
        os_realizada_event: OrdemServicoRealizadaEvent,
    ):
        self.ordem_servico_repository = ordem_servico_repository
        self.os_criada_event = os_criada_event
        self.orcamento_solicitado_event = orcamento_solicitado_event
        self.mecanico_designado_event = mecanico_designado_event
        self.servicos_incluidos_event = servicos_incluidos_event
        self.peca_incluida_event = peca_incluida_event
        self.orcamento_gerado_event = orcamento_gerado_event
        self.orcamento_enviado_event = orcamento_enviado_event
        self.os_aceita_event = os_aceita_event
        self.os_realizada_event = os_realizada_event

    async def create_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        created = await self.ordem_servico_repository.create(ordem_servico)

        if created.status == StatusOrdemServico.RECEBIDA:
            await self.os_criada_event.handle(created)

        return created

    async def update_ordem_servico(
        self, ordem_servico: OrdemServicoEntity
    ) -> OrdemServicoEntity:
        updated = await self.ordem_servico_repository.update(ordem_servico)

        # Dispara eventos baseados em status atualizado
        match updated.status:
            case StatusOrdemServico.EM_DIAGNOSTICO:
                await self.mecanico_designado_event.handle(updated)
            case StatusOrdemServico.AGUARDANDO_APROVACAO:
                await self.orcamento_enviado_event.handle(updated)
            case StatusOrdemServico.EM_EXECUCAO:
                await self.os_aceita_event.handle(updated)
            case StatusOrdemServico.FINALIZADA:
                await self.os_realizada_event.handle(updated)

        return updated

    async def get_ordem_servico_by_id(self, id: str) -> OrdemServicoEntity:
        return await self.ordem_servico_repository.get_by_id(id)

    async def get_all_ordens_servico(self) -> List[OrdemServicoEntity]:
        return await self.ordem_servico_repository.get_all()
