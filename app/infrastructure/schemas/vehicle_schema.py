from typing import Optional, Annotated
from pydantic import BaseModel, field_validator, Field
from app.application.validators.vehicle_validator import validate_vehicle_plate

class VehicleBase(BaseModel):
    license_plate: Annotated[str, Field(min_length=5, max_length=10)]
    brand: Annotated[str, Field(min_length=1, max_length=50)]
    model: Annotated[str, Field(min_length=1, max_length=50)]
    year: Annotated[int, Field(ge=1886)]
    client_id: Optional[str] = None

    @field_validator('license_plate')
    @classmethod
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