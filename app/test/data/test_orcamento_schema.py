import pytest
from decimal import Decimal
from app.infrastructure.schemas.orcamento import (
    OrcamentoOutput, ServicoOrcamento, InventoryItemOrcamento
)
from app.infrastructure.schemas.ordem_servico import OrdemServicoOutput
from app.infrastructure.schemas.servico import ServicoOutput
from app.infrastructure.schemas.inventory_item_schema import InventoryItemOut

class TestOrcamentoSchemas:

    def test_servico_orcamento_valid(self):
        servico = ServicoOutput(id="s1", descricao="Serviço X", preco=Decimal("100.00"))
        servico_orc = ServicoOrcamento(
            servico=servico,
            valor_na_os=Decimal("150.00"),
            observacoes="Observação teste"
        )
        assert servico_orc.servico.id == "s1"
        assert servico_orc.valor_na_os == Decimal("150.00")
        assert servico_orc.observacoes == "Observação teste"

    def test_inventory_item_orcamento_valid(self):
        item = InventoryItemOut(
            id=1,
            name="Item A",
            description="Descrição",
            quantity=10,
            minimum_stock=2,
            unit_price=Decimal("20.00"),
        )
        item_orc = InventoryItemOrcamento(
            item=item,
            quantidade=5,
            valor_unitario_na_os=Decimal("22.00"),
            valor_total=Decimal("110.00"),
        )
        assert item_orc.item.id == 1
        assert item_orc.quantidade == 5
        assert item_orc.valor_total == Decimal("110.00")

    def test_orcamento_output_valid(self):
        ordem = OrdemServicoOutput(
            id="os1",
            cliente_id="cli1",
            vehicle_id=123,
            servico_ids=["s1", "s2"],
            status="recebida",
            data_abertura="2025-01-01T10:00:00",
            data_fechamento=None,
            atendente_id=None,
            mecanico_id=None,
            orcamento_id=None
        )
        servico = ServicoOutput(id="s1", descricao="Serviço X", preco=Decimal("100.00"))
        servico_orc = ServicoOrcamento(servico=servico, valor_na_os=Decimal("150.00"))
        item = InventoryItemOut(
            id=1,
            name="Item A",
            description="Descrição",
            quantity=10,
            minimum_stock=2,
            unit_price=Decimal("20.00"),
        )
        item_orc = InventoryItemOrcamento(
            item=item,
            quantidade=5,
            valor_unitario_na_os=Decimal("22.00"),
            valor_total=Decimal("110.00"),
        )
        orcamento = OrcamentoOutput(
            ordem_servico=ordem,
            servicos=[servico_orc],
            inventory_items=[item_orc],
            total_servicos=Decimal("150.00"),
            total_items=Decimal("110.00"),
            total_geral=Decimal("260.00"),
        )
        assert orcamento.total_geral == Decimal("260.00")
        assert len(orcamento.servicos) == 1
        assert len(orcamento.inventory_items) == 1
