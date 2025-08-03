from fastapi import APIRouter, Depends, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.infrastructure.schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.domain.entities.vehicle import Vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.post("/", response_model=VehicleResponse)
@inject
async def create_vehicle(
    data: VehicleCreate,
    use_case: VehicleUseCase = Depends(Provide[Container.vehicle_use_case])
):
    vehicle = Vehicle(id=0, **data.dict())
    created = await use_case.create(vehicle)
    return created

@router.get("/{vehicle_id}", response_model=VehicleResponse)
@inject
async def get_vehicle(
    vehicle_id: int,
    use_case: VehicleUseCase = Depends(Provide[Container.vehicle_use_case])
):
    vehicle = await use_case.get(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.get("/", response_model=List[VehicleResponse])
@inject
async def list_vehicles(
    use_case: VehicleUseCase = Depends(Provide[Container.vehicle_use_case])
):
    return await use_case.list()

@router.put("/", response_model=VehicleResponse)
@inject
async def update_vehicle(
    data: VehicleUpdate,
    use_case: VehicleUseCase = Depends(Provide[Container.vehicle_use_case])
):
    vehicle = Vehicle(**data.dict())
    updated = await use_case.update(vehicle)
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated

@router.delete("/{vehicle_id}", status_code=204)
@inject
async def delete_vehicle(
    vehicle_id: int,
    use_case: VehicleUseCase = Depends(Provide[Container.vehicle_use_case])
):
    await use_case.delete(vehicle_id)
