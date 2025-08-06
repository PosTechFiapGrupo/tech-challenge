import uuid
from datetime import datetime
from typing import Optional, List
from app.domain.entities.status_ordem_servico import StatusOrdemServico


class OrdemServicoEntity:

    def __init__(
        self,
        uid: str,
        cliente_id: str,
        veiculo_id: str,
        servico_ids: List[str],
        status: StatusOrdemServico = StatusOrdemServico.RECEBIDA,
        mecanico_id: Optional[str] = None,
        atendente_id: Optional[str] = None,
        orcamento_id: Optional[str] = None,
        data_abertura: Optional[datetime] = None,
        data_fechamento: Optional[datetime] = None,
    ):
        self.id = uid
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.servico_ids = servico_ids
        self.mecanico_id = mecanico_id
        self.atendente_id = atendente_id
        self.orcamento_id = orcamento_id
        self.status = status
        self.data_abertura = data_abertura or datetime.utcnow()
        self.data_fechamento = data_fechamento

    def iniciar_execucao(self):
        if self.status != StatusOrdemServico.RECEBIDA:
            raise ValueError(
                f"Não é possível iniciar execução a partir de {self.status}"
            )
        self.status = StatusOrdemServico.EM_EXECUCAO

    def finalizar(self):
        if self.status != StatusOrdemServico.EM_EXECUCAO:
            raise ValueError(f"Não é possível finalizar a partir de {self.status}")
        self.status = StatusOrdemServico.FINALIZADA
        self.data_fechamento = datetime.utcnow()

    def cancelar(self):
        if self.status in [StatusOrdemServico.FINALIZADA, StatusOrdemServico.CANCELADA]:
            raise ValueError(
                "Não é possível cancelar uma OS já finalizada ou cancelada."
            )
        self.status = StatusOrdemServico.CANCELADA


class OrdemServicoEntityFactory:

    @staticmethod
    def create(
        id: Optional[str],
        cliente_id: str,
        veiculo_id: str,
        servico_ids: List[str],
        mecanico_id: Optional[str] = None,
        atendente_id: Optional[str] = None,
        orcamento_id: Optional[str] = None,
        status: StatusOrdemServico = StatusOrdemServico.RECEBIDA,
        data_abertura: Optional[datetime] = None,
    ) -> OrdemServicoEntity:
        if id is None:
            id = str(uuid.uuid4())
        return OrdemServicoEntity(
            uid=id,
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            servico_ids=servico_ids,
            mecanico_id=mecanico_id,
            atendente_id=atendente_id,
            orcamento_id=orcamento_id,
            status=status,
            data_abertura=data_abertura or datetime.utcnow(),
        )
