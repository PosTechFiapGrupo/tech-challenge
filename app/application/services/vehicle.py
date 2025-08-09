from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.domain.entities.vehicle import Vehicle
from app.application.validators.veiculo import VeiculoValidator
from typing import List


class VehicleService:
    def __init__(self, use_case: VehicleUseCase, vehicle_validator: VeiculoValidator):
        self.use_case = use_case
        self.vehicle_validator = vehicle_validator

    async def criar_vehicle(self, vehicle: Vehicle) -> Vehicle:
        # Aqui não validamos existência porque é criação
        return await self.use_case.create(vehicle)

    async def listar_vehicles(self) -> List[Vehicle]:
        return await self.use_case.list()

    async def buscar_vehicle_por_id(self, vehicle_id: int) -> Vehicle:
        await self.vehicle_validator.validate_exists(vehicle_id)
        return await self.use_case.get(vehicle_id)

    async def atualizar_vehicle(self, vehicle: Vehicle) -> Vehicle:
        await self.vehicle_validator.validate_exists(vehicle.id)
        return await self.use_case.update(vehicle)

    async def deletar_vehicle(self, vehicle_id: int) -> None:
        await self.vehicle_validator.validate_exists(vehicle_id)
        await self.use_case.delete(vehicle_id)