from app.domain.entities.ordem_servico import OrdemServicoEntity
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


class OrdemServicoCreatedQueueEvent(OrdemServicoSolicitadaEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Ordem de Serviço criada (ID: {ordem_servico.id})")


class OrdemServicoSolicitadaQueueEvent(OrdemServicoSolicitadaEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        # Aqui vai a lógica (ex: enviar mensagem para uma fila, log, etc.)
        print(f"[EVENT] OS solicitada: {ordem_servico.id}")


class OrcamentoSolicitadoQueueEvent(OrcamentoSolicitadoEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Orçamento solicitado: {ordem_servico.id}")


class MecanicoDesignadoQueueEvent(MecanicoDesignadoEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Mecânico designado para OS: {ordem_servico.id}")


class ServicosIncluidosQueueEvent(ServicosIncluidosEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Serviços incluídos na OS: {ordem_servico.id}")


class PecaOuInsumoIncluidoQueueEvent(PecaOuInsumoIncluidoEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Peça/Insumo incluído na OS: {ordem_servico.id}")


class OrcamentoGeradoQueueEvent(OrcamentoGeradoEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Orçamento gerado para OS: {ordem_servico.id}")


class OrcamentoEnviadoAoClienteQueueEvent(OrcamentoEnviadoAoClienteEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] Orçamento enviado ao cliente para OS: {ordem_servico.id}")


class OrdemServicoAceitaQueueEvent(OrdemServicoAceitaEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] OS aceita pelo cliente: {ordem_servico.id}")


class OrdemServicoRealizadaQueueEvent(OrdemServicoRealizadaEvent):
    async def handle(self, ordem_servico: OrdemServicoEntity) -> None:
        print(f"[EVENT] OS realizada com sucesso: {ordem_servico.id}")
