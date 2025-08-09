from typing import List, Optional
from app.domain.entities.vehicle import Vehicle

class VehicleRepository:
    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        raise NotImplementedError

    async def get_by_plate(self, license_plate: str) -> Optional[Vehicle]:
        raise NotImplementedError

    async def list_all(self) -> List[Vehicle]:
        raise NotImplementedError

    async def create(self, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError

    async def update(self, vehicle: Vehicle) -> Optional[Vehicle]:
        raise NotImplementedError

    async def delete(self, vehicle_id: int) -> None:
        raise NotImplementedError
