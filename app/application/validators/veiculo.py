from fastapi import HTTPException
from app.domain.repositories.vehicle_repository import VehicleRepository


class VeiculoValidator:
    def __init__(self, vehicle_repository: VehicleRepository):
        self.vehicle_repository = vehicle_repository

    async def validate_exists(self, vehicle_id: int) -> None:
        vehicle = await self.vehicle_repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")