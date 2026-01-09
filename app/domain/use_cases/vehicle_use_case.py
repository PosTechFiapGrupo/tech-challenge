from typing import List, Optional

from app.domain.entities.vehicle import Vehicle
from app.domain.exceptions import EntityAlreadyExists, EntityNotFound
from app.domain.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class VehicleUseCase:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    async def get(self, vehicle_id: int) -> Vehicle:
        vehicle = await self.repository.get_by_id(vehicle_id)
        if not vehicle:
            logger.warning("Veículo não encontrado", extra={"vehicle_id": vehicle_id})
            raise EntityNotFound("Vehicle")
        logger.info("Veículo buscado", extra={"vehicle_id": vehicle_id})
        return vehicle

    async def list(self) -> List[Vehicle]:
        vehicles = await self.repository.list_all()
        logger.info("Veículos listados", extra={"count": len(vehicles)})
        return vehicles

    async def create(self, vehicle: Vehicle) -> Vehicle:
        existing = await self.repository.get_by_plate(vehicle.license_plate)
        if existing:
            logger.warning("Tentativa de criar veículo com placa duplicada", extra={"placa": vehicle.license_plate})
            raise EntityAlreadyExists("Já existe um veículo com esta placa.")
        created = await self.repository.create(vehicle)
        logger.info("Veículo criado", extra={"vehicle_id": created.id, "placa": vehicle.license_plate})
        return created

    async def update(self, vehicle: Vehicle) -> Optional[Vehicle]:
        updated = await self.repository.update(vehicle)
        logger.info("Veículo atualizado", extra={"vehicle_id": vehicle.id})
        return updated

    async def delete(self, vehicle_id: int) -> None:
        await self.repository.delete(vehicle_id)
        logger.info("Veículo deletado", extra={"vehicle_id": vehicle_id})
