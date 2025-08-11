from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities.servico import ServicoEntity, ServicoEntityFactory
from app.infrastructure.container import Container
from app.application.services.servico import ServicoService
from app.infrastructure.auth_dependencies import role_required
from app.infrastructure.schemas.servico import (
    ServicoOutput,
    ServicoInput,
    ServicoUpdate,
)

router = APIRouter(prefix="/servicos", tags=["servicos"])


@router.get("/", response_model=List[ServicoOutput], dependencies=[Depends(role_required("admin"))])
@inject
async def get_all_servicos(
    servico_service: ServicoService = Depends(Provide[Container.servico_service]),
) -> List[dict]:
    try:
        servicos: List[ServicoEntity] = await servico_service.get_all_servicos()
        return [servico.__dict__ for servico in servicos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}", response_model=ServicoOutput, dependencies=[Depends(role_required("admin"))])
@inject
async def get_servico_by_id(
    id: str,
    servico_service: ServicoService = Depends(Provide[Container.servico_service]),
) -> dict:
    try:
        servico: ServicoEntity | None = await servico_service.get_servico_by_id(id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado"
            )
        return servico.__dict__
    except HTTPException:
        raise  # Re-raise HTTPException as is
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/", response_model=ServicoOutput, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin"))])
@inject
async def create_servico(
    servico_data: ServicoInput,
    servico_factory: ServicoEntityFactory = Depends(Provide[Container.servico_factory]),
    servico_service: ServicoService = Depends(Provide[Container.servico_service]),
) -> dict:
    try:
        servico_entity: ServicoEntity = servico_factory.create(
            id=None, descricao=servico_data.descricao, preco=servico_data.preco
        )
        created_servico: ServicoEntity = await servico_service.create_servico(
            servico_entity
        )
        return created_servico.__dict__
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id}", response_model=ServicoOutput, dependencies=[Depends(role_required("admin"))])
@inject
async def update_servico(
    id: str,
    servico_data: ServicoInput,
    servico_factory: ServicoEntityFactory = Depends(Provide[Container.servico_factory]),
    servico_service: ServicoService = Depends(Provide[Container.servico_service]),
) -> dict:
    try:
        # Verificar se o serviço existe
        existing_servico = await servico_service.get_servico_by_id(id)
        if not existing_servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado"
            )

        servico_entity: ServicoEntity = servico_factory.create(
            id=id, descricao=servico_data.descricao, preco=servico_data.preco
        )
        updated_servico: ServicoEntity = await servico_service.update_servico(
            servico_entity
        )
        return updated_servico.__dict__
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required("admin"))])
@inject
async def delete_servico(
    id: str,
    servico_service: ServicoService = Depends(Provide[Container.servico_service]),
):
    try:
        result = await servico_service.delete_servico(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
