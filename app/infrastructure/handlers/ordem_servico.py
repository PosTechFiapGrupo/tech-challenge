from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from app.infrastructure.container import Container
from app.application.services.ordem_servico import OrdemServicoService
from app.infrastructure.schemas.ordem_servico import (
    OrdemServicoInput,
    OrdemServicoUpdate,
    OrdemServicoOutput,
)
from app.domain.entities.ordem_servico import OrdemServicoEntityFactory

router = APIRouter(prefix="/ordens-servico", tags=["ordens_servico"])


@router.post(
    "/", response_model=OrdemServicoOutput, status_code=status.HTTP_201_CREATED
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
            veiculo_id=ordem_servico_data.veiculo_id,
            servico_ids=ordem_servico_data.servico_ids,
            mecanico_id=ordem_servico_data.mecanico_id,
            atendente_id=ordem_servico_data.atendente_id,
            orcamento_id=ordem_servico_data.orcamento_id,
            status=ordem_servico_data.status,
        )

        created = await service.criar_ordem_servico(entity)
        return created.__dict__

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrdemServicoOutput])
@inject
async def get_all_ordens_servico(
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
) -> List[dict]:
    try:
        ordens = await service.listar_ordens_servico()
        return [os.__dict__ for os in ordens]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=OrdemServicoOutput)
@inject
async def get_ordem_servico_by_id(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
) -> dict:
    os = await service.buscar_ordem_servico_por_id(id)
    if not os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    return os.__dict__


@router.put("/{id}", response_model=OrdemServicoOutput)
@inject
async def update_ordem_servico(
    id: str,
    update_data: OrdemServicoUpdate,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
) -> dict:
    try:
        updated = await service.atualizar_ordem_servico(id, update_data)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}/iniciar-execucao", response_model=OrdemServicoOutput)
@inject
async def iniciar_execucao_ordem_servico(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.iniciar_execucao(id)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/finalizar", response_model=OrdemServicoOutput)
@inject
async def finalizar_ordem_servico(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.finalizar(id)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/cancelar", response_model=OrdemServicoOutput)
@inject
async def cancelar_ordem_servico(
    id: str,
    service: OrdemServicoService = Depends(Provide[Container.ordem_servico_service]),
):
    try:
        updated = await service.cancelar(id)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
