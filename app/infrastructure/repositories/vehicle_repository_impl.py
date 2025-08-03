from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.vehicle import Vehicle
from app.domain.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.models.vehicle_model import VehicleModel

class VehicleRepositoryImpl(VehicleRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        result = await self.db.execute(select(VehicleModel).filter_by(id=vehicle_id))
        vehicle_model = result.scalar_one_or_none()
        if vehicle_model:
            return Vehicle(
                id=vehicle_model.id,
                license_plate=vehicle_model.license_plate,
                brand=vehicle_model.brand,
                model=vehicle_model.model,
                year=vehicle_model.year
            )
        return None

    async def list_all(self) -> List[Vehicle]:
        result = await self.db.execute(select(VehicleModel))
        vehicles = result.scalars().all()
        return [
            Vehicle(
                id=v.id,
                license_plate=v.license_plate,
                brand=v.brand,
                model=v.model,
                year=v.year
            ) for v in vehicles
        ]

    async def create(self, vehicle: Vehicle) -> Vehicle:
        vehicle_model = VehicleModel(
            license_plate=vehicle.license_plate,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year
        )
        self.db.add(vehicle_model)
        await self.db.commit()
        await self.db.refresh(vehicle_model)
        return Vehicle(
            id=vehicle_model.id,
            license_plate=vehicle_model.license_plate,
            brand=vehicle_model.brand,
            model=vehicle_model.model,
            year=vehicle_model.year
        )

    async def update(self, vehicle: Vehicle) -> Optional[Vehicle]:
        vehicle_model = await self.db.get(VehicleModel, vehicle.id)
        if not vehicle_model:
            return None
        vehicle_model.license_plate = vehicle.license_plate
        vehicle_model.brand = vehicle.brand
        vehicle_model.model = vehicle.model
        vehicle_model.year = vehicle.year
        await self.db.commit()
        await self.db.refresh(vehicle_model)
        return Vehicle(
            id=vehicle_model.id,
            license_plate=vehicle_model.license_plate,
            brand=vehicle_model.brand,
            model=vehicle_model.model,
            year=vehicle_model.year
        )

    async def delete(self, vehicle_id: int) -> None:
        vehicle_model = await self.db.get(VehicleModel, vehicle_id)
        if vehicle_model:
            await self.db.delete(vehicle_model)
            await self.db.commit()
