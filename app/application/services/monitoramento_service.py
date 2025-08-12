from app.domain.use_cases.calcular_tempo_medio_ordem_servico import CalcularTempoMedioOrdemServico

class MonitoramentoService:
    def __init__(self, ordem_servico_repo):
        self.use_case = CalcularTempoMedioOrdemServico(ordem_servico_repo)

    async def obter_tempo_medio(self):
        return await self.use_case.executar()
