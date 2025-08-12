import pytest
from app.domain.entities.status_ordem_servico import StatusOrdemServico

class TestStatusOrdemServico:

    def test_enum_values(self):
        assert StatusOrdemServico.RECEBIDA.value == "recebida"
        assert StatusOrdemServico.EM_DIAGNOSTICO.value == "em_diagnostico"
        assert StatusOrdemServico.AGUARDANDO_APROVACAO.value == "aguardando_aprovacao"
        assert StatusOrdemServico.EM_EXECUCAO.value == "em_execucao"
        assert StatusOrdemServico.FINALIZADA.value == "finalizada"
        assert StatusOrdemServico.ENTREGUE.value == "entregue"
        assert StatusOrdemServico.CANCELADA.value == "cancelada"

    def test_enum_membership(self):
        with pytest.raises(ValueError):
            StatusOrdemServico("invalido")
