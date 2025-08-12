from fastapi import APIRouter, Depends, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.infrastructure.schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse
from app.application.services.vehicle import VehicleService
from app.domain.entities.vehicle import Vehicle
from app.application.validators.vehicle_validator import validate_vehicle_plate
from app.domain.exceptions import EntityAlreadyExists, EntityNotFound
from app.infrastructure.auth_dependencies import role_required

router = APIRouter(prefix="/vehicles", tags=["vehicles"])



@router.post("/", response_model=VehicleResponse, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def create_vehicle(
    data: VehicleCreate,
    service: VehicleService = Depends(Provide[Container.vehicle_service])
):
    if not validate_vehicle_plate(data.license_plate):
        raise HTTPException(status_code=400, detail="Formato de placa inválido")

    try:
        vehicle = Vehicle(id=0, **data.dict())
        created = await service.criar_vehicle(vehicle)
        return created
    except EntityAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{vehicle_id}", response_model=VehicleResponse, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def get_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(Provide[Container.vehicle_service])
):
    try:
        return await service.buscar_vehicle_por_id(vehicle_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[VehicleResponse], dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def list_vehicles(
    service: VehicleService = Depends(Provide[Container.vehicle_service])
):
    return await service.listar_vehicles()


@router.put("/", response_model=VehicleResponse, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def update_vehicle(
    data: VehicleUpdate,
    service: VehicleService = Depends(Provide[Container.vehicle_service])
):
    vehicle = Vehicle(**data.dict())
    updated = await service.atualizar_vehicle(vehicle)
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated


@router.delete("/{vehicle_id}", status_code=204, dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def delete_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(Provide[Container.vehicle_service])
):
    await service.deletar_vehicle(vehicle_id)