class CalcularTempoMedioOrdemServico:
    def __init__(self, ordem_servico_repo):
        self.ordem_servico_repo = ordem_servico_repo

    async def executar(self):
        return await self.ordem_servico_repo.calcular_tempo_medio_execucao()
