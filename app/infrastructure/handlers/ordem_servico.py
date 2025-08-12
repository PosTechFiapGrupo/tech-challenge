from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from app.infrastructure.auth_dependencies import role_required
from app.infrastructure.container import Container
from app.application.services.ordem_servico import OrdemServicoService
from app.infrastructure.schemas.ordem_servico import (
    OrdemServicoInput,
    OrdemServicoUpdate,
    OrdemServicoOutput,
    OrdemServicoStatusQuery,
)
from app.infrastructure.schemas.ordem_servico_servico import (
    AddServicoToOrdemServicoInput,
    OrdemServicoServicoOutput,
)
from app.infrastructure.schemas.ordem_servico_inventory_item import (
    AddInventoryItemToOrdemServicoInput,
    OrdemServicoInventoryItemOutput,
)
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory
from app.domain.entities.status_ordem_servico import StatusOrdemServico

router = APIRouter(prefix="/ordens-servico", tags=["ordens_servico"])


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
            status=ordem_servico_data.status or StatusOrdemServico.RECEBIDA,
        )

        created = await service.criar_ordem_servico(entity)
        print(f"created = {created} ({type(created)})")

        return OrdemServicoOutput.model_validate(created).model_dump()

    except Exception as e:
        import traceback
        print("ERRO AO CRIAR OS:", traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


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
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/cancelar", response_model=OrdemServicoOutput, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def cancelar_ordem_servico(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.cancelar(id)
        return OrdemServicoOutput.model_validate(updated).model_dump()
    except ValueError as e:
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
