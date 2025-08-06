from typing import List, Optional
from app.domain.entities.vehicle import Vehicle
from app.domain.repositories.vehicle_repository import VehicleRepository

class VehicleUseCase:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    async def get(self, vehicle_id: int) -> Optional[Vehicle]:
        return await self.repository.get_by_id(vehicle_id)

    async def list(self) -> List[Vehicle]:
        return await self.repository.list_all()

    async def create(self, vehicle: Vehicle) -> Vehicle:
        return await self.repository.create(vehicle)

    async def update(self, vehicle: Vehicle) -> Optional[Vehicle]:
        return await self.repository.update(vehicle)

    async def delete(self, vehicle_id: int) -> None:
        await self.repository.delete(vehicle_id)
