from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities.cliente import ClienteEntity, ClienteEntityFactory
from app.infrastructure.container import Container
from app.application.services.cliente import ClienteService
from app.infrastructure.auth_dependencies import role_required
from app.infrastructure.schemas.cliente import (
    ClienteOutput,
    ClienteInput,
    ClienteUpdate,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteOutput], dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def get_all_clientes(
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
) -> List[dict]:
    try:
        clientes: List[ClienteEntity] = await cliente_service.get_all_clientes()
        return [cliente.__dict__ for cliente in clientes]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}", response_model=ClienteOutput, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def get_cliente_by_id(
    id: str,
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
) -> dict:
    try:
        cliente: ClienteEntity | None = await cliente_service.get_cliente_by_id(id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
            )
        return cliente.__dict__
    except HTTPException:
        raise  # Re-raise HTTPException as is
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/cpf/{cpf}", response_model=ClienteOutput, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def get_cliente_by_cpf(
    cpf: str,
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
) -> dict:
    try:
        cliente: ClienteEntity = await cliente_service.get_cliente_by_cpf(cpf)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
            )
        return cliente.__dict__
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/", response_model=ClienteOutput, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def create_cliente(
    cliente_data: ClienteInput,
    cliente_factory: ClienteEntityFactory = Depends(Provide[Container.cliente_factory]),
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
) -> dict:
    try:
        cliente_entity: ClienteEntity = cliente_factory.create(
            id=None,
            nome=cliente_data.nome,
            telefone=cliente_data.telefone,
            email=cliente_data.email,
            cpf=cliente_data.cpf,
        )
        created_cliente: ClienteEntity = await cliente_service.create_cliente(
            cliente_entity
        )
        return created_cliente.__dict__
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id}", response_model=ClienteOutput, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def update_cliente(
    id: str,
    cliente_data: ClienteInput,
    cliente_factory: ClienteEntityFactory = Depends(Provide[Container.cliente_factory]),
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
) -> dict:
    try:
        # Verificar se o cliente existe
        existing_cliente = await cliente_service.get_cliente_by_id(id)
        if not existing_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
            )

        cliente_entity: ClienteEntity = cliente_factory.create(
            id=id,
            nome=cliente_data.nome,
            telefone=cliente_data.telefone,
            email=cliente_data.email,
            cpf=cliente_data.cpf,
        )
        updated_cliente: ClienteEntity = await cliente_service.update_cliente(
            cliente_entity
        )
        return updated_cliente.__dict__
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def delete_cliente(
    id: str,
    cliente_service: ClienteService = Depends(Provide[Container.cliente_service]),
):
    try:
        result = await cliente_service.delete_cliente(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
