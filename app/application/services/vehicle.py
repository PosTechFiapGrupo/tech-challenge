from typing import List

from app.application.validators.veiculo import VeiculoValidator
from app.domain.entities.vehicle import Vehicle
from app.domain.use_cases.vehicle_use_case import VehicleUseCase
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class VehicleService:
    def __init__(self, use_case: VehicleUseCase, vehicle_validator: VeiculoValidator):
        self.use_case = use_case
        self.vehicle_validator = vehicle_validator

    async def criar_vehicle(self, vehicle: Vehicle) -> Vehicle:
        created = await self.use_case.create(vehicle)
        logger.info("Veículo criado", extra={"vehicle_id": created.id, "placa": vehicle.license_plate})
        return created

    async def listar_vehicles(self) -> List[Vehicle]:
        vehicles = await self.use_case.list()
        logger.info("Veículos listados", extra={"count": len(vehicles)})
        return vehicles

    async def buscar_vehicle_por_id(self, vehicle_id: int) -> Vehicle:
        await self.vehicle_validator.validate_exists(vehicle_id)
        vehicle = await self.use_case.get(vehicle_id)
        logger.info("Veículo buscado", extra={"vehicle_id": vehicle_id})
        return vehicle

    async def atualizar_vehicle(self, vehicle: Vehicle) -> Vehicle:
        await self.vehicle_validator.validate_exists(vehicle.id)
        updated = await self.use_case.update(vehicle)
        logger.info("Veículo atualizado", extra={"vehicle_id": vehicle.id})
        return updated

    async def deletar_vehicle(self, vehicle_id: int) -> None:
        await self.vehicle_validator.validate_exists(vehicle_id)
        await self.use_case.delete(vehicle_id)
        logger.info("Veículo deletado", extra={"vehicle_id": vehicle_id})