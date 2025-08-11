from abc import ABC, abstractmethod
from app.domain.entities.ordem_servico import OrdemServicoEntity


class OrdemServicoEvent(ABC):
    @abstractmethod
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        raise NotImplementedError


class OrdemServicoSolicitadaEvent(OrdemServicoEvent):
    pass


class OrcamentoSolicitadoEvent(OrdemServicoEvent):
    pass


class MecanicoDesignadoEvent(OrdemServicoEvent):
    pass


class ServicosIncluidosEvent(OrdemServicoEvent):
    pass


class PecaOuInsumoIncluidoEvent(OrdemServicoEvent):
    pass


class OrcamentoGeradoEvent(OrdemServicoEvent):
    pass


class OrcamentoEnviadoAoClienteEvent(OrdemServicoEvent):
    pass


class OrdemServicoAceitaEvent(OrdemServicoEvent):
    pass


class OrdemServicoRealizadaEvent(OrdemServicoEvent):
    pass
