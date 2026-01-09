import traceback
from typing import List

import newrelic.agent
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.ordem_servico import OrdemServicoService
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory
from app.domain.entities.status_ordem_servico import StatusOrdemServico
from app.domain.exceptions import ClienteNotFound, ServicoNotFound, VehicleNotFound
from app.infrastructure.auth_dependencies import role_required
from app.infrastructure.container import Container
from app.infrastructure.logging_config import get_logger
from app.infrastructure.schemas.ordem_servico import (
    OrdemServicoInput,
    OrdemServicoOutput,
    OrdemServicoStatusQuery,
    OrdemServicoUpdate,
)
from app.infrastructure.schemas.ordem_servico_inventory_item import (
    AddInventoryItemToOrdemServicoInput,
    OrdemServicoInventoryItemOutput,
)
from app.infrastructure.schemas.ordem_servico_servico import (
    AddServicoToOrdemServicoInput,
    OrdemServicoServicoOutput,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/ordens-servico", tags=["ordens_servico"])


def _record_ordem_servico_event(event_type: str, ordem_servico_id: str = None, extra_data: dict = None):
    """Registra evento de ordem de serviço no New Relic."""
    try:
        event_data = {"event_type": event_type, "ordem_servico_id": ordem_servico_id or ""}
        if extra_data:
            event_data.update(extra_data)
        
        newrelic.agent.record_custom_event("OrdemServicoEvent", event_data)
        newrelic.agent.record_custom_metric(f"Custom/OrdemServico/{event_type}", 1)
    except Exception:
        pass


@router.post(
    "/", response_model=OrdemServicoOutput, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))]
)
@inject
async def create_ordem_servico(
    ordem_servico_data: OrdemServicoInput,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
) -> dict:
    try:
        entity = OrdemServicoEntityFactory.create(
            id=None,
            cliente_id=ordem_servico_data.cliente_id,
            vehicle_id=int(ordem_servico_data.vehicle_id),
            servico_ids=ordem_servico_data.servico_ids,
            mecanico_id=ordem_servico_data.mecanico_id,
            atendente_id=ordem_servico_data.atendente_id,
            orcamento_id=ordem_servico_data.orcamento_id,
            status=StatusOrdemServico(ordem_servico_data.status),
        )
        
        created = await service.criar_ordem_servico(entity)
        
        # Log e evento para monitoramento
        logger.info(
            "Ordem de serviço criada com sucesso",
            extra={
                "ordem_servico_id": str(created.id),
                "cliente_id": str(created.cliente_id),
                "status": created.status.value,
                "event_type": "ordem_servico_created"
            }
        )
        _record_ordem_servico_event("Created", str(created.id), {"status": created.status.value})
        
        return OrdemServicoOutput.model_validate(created).model_dump()
    
    except (ClienteNotFound, ServicoNotFound, VehicleNotFound) as e:
        logger.warning(
            "Recurso não encontrado ao criar ordem de serviço",
            extra={"error": str(e), "error_type": type(e).__name__}
        )
        _record_ordem_servico_event("CreationFailed", None, {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except ValueError as e:
        logger.warning(
            "Dados inválidos ao criar ordem de serviço",
            extra={"error": str(e)}
        )
        _record_ordem_servico_event("CreationFailed", None, {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            "Erro inesperado ao criar ordem de serviço",
            extra={"error": str(e), "traceback": traceback.format_exc()},
            exc_info=True
        )
        _record_ordem_servico_event("CreationError", None, {"error": str(e)})
        raise HTTPException(
            status_code=500, 
            detail="Erro interno ao criar ordem de serviço"
        )


@router.get("/", response_model=List[OrdemServicoOutput], dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def get_all_ordens_servico(
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        ordens = await service.listar_ordens_servico()
        return [OrdemServicoOutput.model_validate(os).model_dump() for os in ordens]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{status}", response_model=List[OrdemServicoOutput], dependencies=[Depends(role_required("admin", "atendente", "mecanico", "cliente"))])
@inject
async def get_ordens_servico_by_status(
        status: str,
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        # Validar o status usando o schema
        status_query = OrdemServicoStatusQuery(status=status)
        ordens = await service.listar_ordens_servico_por_status(status_query.status)
        return [OrdemServicoOutput.model_validate(os).model_dump() for os in ordens]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico", "cliente"))])
@inject
async def get_ordem_servico_by_id(
        id: str,
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    os = await service.buscar_ordem_servico_por_id(id)
    if not os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    return OrdemServicoOutput.model_validate(os).model_dump()


@router.put("/{id}", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def update_ordem_servico(
        id: str,
        update_data: OrdemServicoUpdate,
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.atualizar_ordem_servico(id, update_data)
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}/iniciar-execucao", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def iniciar_execucao_ordem_servico(
        id: str,
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.iniciar_execucao(id)
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/finalizar", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def finalizar_ordem_servico(
        id: str,
        service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.finalizar(id)
        
        logger.info(
            "Ordem de serviço finalizada",
            extra={
                "ordem_servico_id": id,
                "status": updated.status.value,
                "event_type": "ordem_servico_finalizada"
            }
        )
        _record_ordem_servico_event("Finalizada", id, {"status": updated.status.value})
        
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        logger.warning(
            "Falha ao finalizar ordem de serviço",
            extra={"ordem_servico_id": id, "error": str(e)}
        )
        _record_ordem_servico_event("FinalizacaoFailed", id, {"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/cancelar", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def cancelar_ordem_servico(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.cancelar(id)
        
        logger.info(
            "Ordem de serviço cancelada",
            extra={
                "ordem_servico_id": id,
                "status": updated.status.value,
                "event_type": "ordem_servico_cancelada"
            }
        )
        _record_ordem_servico_event("Cancelada", id, {"status": updated.status.value})
        
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        logger.warning(
            "Falha ao cancelar ordem de serviço",
            extra={"ordem_servico_id": id, "error": str(e)}
        )
        _record_ordem_servico_event("CancelamentoFailed", id, {"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_servico_id}/servicos", response_model=OrdemServicoServicoOutput, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def adicionar_servico_a_ordem_servico(
    ordem_servico_id: str,
    servico_data: AddServicoToOrdemServicoInput,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    """Adiciona um serviço a uma ordem de serviço. O valor será automaticamente copiado do preço atual do serviço."""
    try:
        relacao = await service.adicionar_servico(
            ordem_servico_id=ordem_servico_id,
            servico_id=servico_data.servico_id,
            observacoes=servico_data.observacoes
        )
        return OrdemServicoServicoOutput.model_validate(relacao).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ordem_servico_id}/itens", response_model=OrdemServicoInventoryItemOutput, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def adicionar_item_a_ordem_servico(
    ordem_servico_id: str,
    item_data: AddInventoryItemToOrdemServicoInput,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    """Adiciona um item de inventário a uma ordem de serviço. O valor será automaticamente copiado do preço atual do item."""
    try:
        relacao = await service.adicionar_item_inventario(
            ordem_servico_id=ordem_servico_id,
            inventory_item_id=item_data.inventory_item_id,
            quantidade=item_data.quantidade
        )
        return OrdemServicoInventoryItemOutput.model_validate(relacao).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}/aprovar-orcamento", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def aprovar_orcamento(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    """Aprova o orçamento e muda a OS para 'em_execucao'."""
    try:
        updated = await service.aprovar_orcamento(id)
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao aprovar orçamento: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Erro interno ao aprovar orçamento.")

@router.put("/{id}/recusar-orcamento", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente"))],)
@inject
async def recusar_orcamento(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    """Recusa o orçamento e muda a OS para 'cancelada'."""
    try:
        updated = await service.recusar_orcamento(id)
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao recusar orçamento: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Erro interno ao recusar orçamento.")
