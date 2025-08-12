import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from app.infrastructure.repositories.ordem_servico_impl import OrdemServicoRepositoryImpl
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory
from app.domain.entities.status_ordem_servico import StatusOrdemServico

# Async iterator para simular o async for sobre database.get_session()
class AsyncSessionIterator:
    def __init__(self, session):
        self.session = session
        self._yielded = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._yielded:
            self._yielded = True
            return self.session
        else:
            raise StopAsyncIteration

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def mock_database(mock_session):
    db = MagicMock()
    db.get_session.return_value = AsyncSessionIterator(mock_session)
    return db

@pytest.fixture
def repo(mock_database):
    repo = OrdemServicoRepositoryImpl()
    repo.database = mock_database
    return repo


@pytest.mark.asyncio
@patch("app.infrastructure.repositories.ordem_servico_impl.OrdemServicoModel")
async def test_create(mock_ordem_servico_model, repo, mock_session):
    # Mock resultado da consulta para _get_servico_ids_for_ordem
    mock_result_servico_ids = MagicMock()
    mock_result_servico_ids.scalars.return_value.all.return_value = ["1", "2", "3"]
    mock_session.execute.return_value = mock_result_servico_ids

    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    # Configura o mock do model criado dentro do método create
    instance = MagicMock()
    instance.id = "123"
    instance.status = StatusOrdemServico.RECEBIDA.value  # Valor válido do enum
    mock_ordem_servico_model.return_value = instance

    ordem = OrdemServicoEntityFactory.create(
        id=None,
        cliente_id="c1",
        vehicle_id="v1",
        mecanico_id="m1",
        atendente_id="a1",
        orcamento_id="o1",
        status=StatusOrdemServico.RECEBIDA,
        data_abertura=datetime.now(),
        servico_ids=["1", "2", "3"],
    )

    result = await repo.create(ordem)

    mock_ordem_servico_model.assert_called_once_with(
        id=ordem.id,
        cliente_id=ordem.cliente_id,
        vehicle_id=ordem.vehicle_id,
        mecanico_id=ordem.mecanico_id,
        atendente_id=ordem.atendente_id,
        orcamento_id=ordem.orcamento_id,
        status=ordem.status.value,
        data_abertura=ordem.data_abertura,
        data_fechamento=None,
    )

    mock_session.flush.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.execute.assert_awaited()  # para _get_servico_ids_for_ordem

    assert result.id == "123"
    assert result.servico_ids == ["1", "2", "3"]
    assert result.status == StatusOrdemServico.RECEBIDA


@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_session):
    model = MagicMock()
    model.id = "123"
    model.cliente_id = "c1"
    model.vehicle_id = "v1"
    model.mecanico_id = "m1"
    model.atendente_id = "a1"
    model.orcamento_id = "o1"
    model.status = StatusOrdemServico.RECEBIDA.value
    model.data_abertura = datetime.now()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = model
    mock_session.execute.return_value = mock_result

    repo._get_servico_ids_for_ordem = AsyncMock(return_value=["1", "2"])

    result = await repo.get_by_id("123")

    mock_session.execute.assert_awaited()
    repo._get_servico_ids_for_ordem.assert_awaited_once()

    assert result.id == "123"
    assert result.servico_ids == ["1", "2"]
    assert result.status == StatusOrdemServico.RECEBIDA


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await repo.get_by_id("999")

    mock_session.execute.assert_awaited_once()
    assert result is None


@pytest.mark.asyncio
async def test_get_all(repo, mock_session):
    model1 = MagicMock()
    model1.id = "1"
    model1.cliente_id = "c1"
    model1.vehicle_id = "v1"
    model1.mecanico_id = None
    model1.atendente_id = None
    model1.orcamento_id = None
    model1.status = StatusOrdemServico.RECEBIDA.value
    model1.data_abertura = datetime.now()

    model2 = MagicMock()
    model2.id = "2"
    model2.cliente_id = "c2"
    model2.vehicle_id = "v2"
    model2.mecanico_id = "m2"
    model2.atendente_id = "a2"
    model2.orcamento_id = "o2"
    model2.status = StatusOrdemServico.FINALIZADA.value
    model2.data_abertura = datetime.now()

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [model1, model2]
    mock_session.execute.return_value = mock_result

    repo._get_servico_ids_for_ordem = AsyncMock(side_effect=[["10"], ["20", "21"]])

    results = await repo.get_all()

    mock_session.execute.assert_awaited_once()
    assert len(results) == 2
    assert results[0].servico_ids == ["10"]
    assert results[1].servico_ids == ["20", "21"]


@pytest.mark.asyncio
async def test_update_success(repo, mock_session):
    model = MagicMock()
    model.id = "123"
    model.cliente_id = "c1"
    model.vehicle_id = "v1"
    model.mecanico_id = None
    model.atendente_id = None
    model.orcamento_id = None
    model.status = StatusOrdemServico.RECEBIDA.value
    model.data_abertura = datetime.now()

    mock_session.get.return_value = model
    mock_session.commit.return_value = None

    repo._get_servico_ids_for_ordem = AsyncMock(return_value=["1", "2"])

    ordem = OrdemServicoEntityFactory.create(
        id="123",
        cliente_id="c1",
        vehicle_id="v1",
        mecanico_id=None,
        atendente_id=None,
        orcamento_id=None,
        status=StatusOrdemServico.FINALIZADA,
        data_abertura=model.data_abertura,
        servico_ids=[]
    )

    result = await repo.update(ordem)

    mock_session.get.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    repo._get_servico_ids_for_ordem.assert_awaited_once()

    assert result.status == StatusOrdemServico.FINALIZADA
    assert result.id == "123"


@pytest.mark.asyncio
async def test_update_not_found(repo, mock_session):
    mock_session.get.return_value = None

    ordem = OrdemServicoEntityFactory.create(
        id="999",
        cliente_id="c1",
        vehicle_id="v1",
        mecanico_id=None,
        atendente_id=None,
        orcamento_id=None,
        status=StatusOrdemServico.FINALIZADA,
        data_abertura=datetime.now(),
        servico_ids=[]
    )

    with pytest.raises(ValueError):
        await repo.update(ordem)

    mock_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_calcular_tempo_medio_execucao_com_result(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = 3600.0  # 1 hora em segundos
    mock_session.execute.return_value = mock_result

    result = await repo.calcular_tempo_medio_execucao()

    mock_session.execute.assert_awaited_once()
    assert isinstance(result, timedelta)
    assert result.total_seconds() == 3600


@pytest.mark.asyncio
async def test_calcular_tempo_medio_execucao_sem_result(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = None
    mock_session.execute.return_value = mock_result

    result = await repo.calcular_tempo_medio_execucao()

    mock_session.execute.assert_awaited_once()
    assert result is None
