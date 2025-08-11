from typing import Optional
from pydantic import BaseModel, constr, conint, validator
from app.application.validators.vehicle_validator import validate_vehicle_plate

class VehicleBase(BaseModel):
    license_plate: constr(min_length=5, max_length=10)
    brand: constr(min_length=1, max_length=50)
    model: constr(min_length=1, max_length=50)
    year: conint(ge=1886)
    client_id: Optional[str] = None

    @validator('license_plate')
    def plate_must_be_valid(cls, license_plate):
        if not validate_vehicle_plate(license_plate):
            raise ValueError('Formato de placa de veículo inválido')
        return license_plate

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    id: int

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        model_config = {
            "from_attributes": True
        }
        json_schema_extra = {
            "example": {
                "license_plate": "ABC1D23",
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "cliente_id": "cli-123"
            }
        }