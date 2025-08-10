from fastapi import HTTPException
from app.domain.repositories.cliente import ClienteRepository
from app.domain.repositories.servico import ServicoRepository
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoValidator:
    def __init__(
        self,
        cliente_repository: ClienteRepository,
        servico_repository: ServicoRepository,
    ):
        self.cliente_repository = cliente_repository
        self.servico_repository = servico_repository

    async def validate_cliente_exists(self, cliente_id: str) -> None:
        if await self.cliente_repository.get_by_id(cliente_id) is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

    async def validate_servicos_exist(self, servico_ids: list[str]) -> None:
        for sid in servico_ids:
            if await self.servico_repository.get_by_id(sid) is None:
                raise HTTPException(
                    status_code=404, detail=f"Serviço {sid} não encontrado"
                )

    @staticmethod
    def validate_status_transition(
        atual: StatusOrdemServico, novo: StatusOrdemServico
    ) -> None:
        transicoes_validas = {
            StatusOrdemServico.RECEBIDA: [StatusOrdemServico.EM_DIAGNOSTICO],
            StatusOrdemServico.EM_DIAGNOSTICO: [
                StatusOrdemServico.AGUARDANDO_APROVACAO
            ],
            StatusOrdemServico.AGUARDANDO_APROVACAO: [
                StatusOrdemServico.EM_EXECUCAO,
                StatusOrdemServico.CANCELADA,
            ],
            StatusOrdemServico.EM_EXECUCAO: [StatusOrdemServico.FINALIZADA],
            StatusOrdemServico.FINALIZADA: [StatusOrdemServico.ENTREGUE],
        }

        if novo not in transicoes_validas.get(atual, []):
            raise HTTPException(
                status_code=400,
                detail=f"Transição inválida de status: {atual} → {novo}",
            )
