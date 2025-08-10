from typing import List, Optional
from app.domain.entities.vehicle import Vehicle
from app.domain.repositories.vehicle_repository import VehicleRepository
from app.domain.exceptions import EntityAlreadyExists
from app.domain.exceptions import EntityNotFound


class VehicleUseCase:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    async def get(self, vehicle_id: int) -> Vehicle:
        vehicle = await self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFound("Vehicle")
        return vehicle

    async def list(self) -> List[Vehicle]:
        return await self.repository.list_all()

    async def create(self, vehicle: Vehicle) -> Vehicle:
        existing = await self.repository.get_by_plate(vehicle.license_plate)
        if existing:
            raise EntityAlreadyExists("Já existe um veículo com esta placa.")
        return await self.repository.create(vehicle)

    async def update(self, vehicle: Vehicle) -> Optional[Vehicle]:
        return await self.repository.update(vehicle)

    async def delete(self, vehicle_id: int) -> None:
        await self.repository.delete(vehicle_id)
