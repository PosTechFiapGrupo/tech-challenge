from decimal import Decimal
from typing import Optional


class OrdemServicoServicoEntity:
    def __init__(
        self,
        id: Optional[int],
        ordem_servico_id: str,
        servico_id: str,
        valor_servico: Decimal,
        observacoes: Optional[str] = None,
    ):
        self.id = id
        self.ordem_servico_id = ordem_servico_id
        self.servico_id = servico_id
        self.valor_servico = valor_servico
        self.observacoes = observacoes


class OrdemServicoServicoEntityFactory:
    @staticmethod
    def create(
        id: Optional[int],
        ordem_servico_id: str,
        servico_id: str,
        valor_servico: Decimal,
        observacoes: Optional[str] = None,
    ) -> OrdemServicoServicoEntity:
        return OrdemServicoServicoEntity(
            id=id,
            ordem_servico_id=ordem_servico_id,
            servico_id=servico_id,
            valor_servico=valor_servico,
            observacoes=observacoes,
        )
