import pytest
from pydantic import ValidationError
from app.infrastructure.schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse

class TestVehicleSchemas:

    def test_vehicle_create_valid(self):
        vehicle = VehicleCreate(
            license_plate="ABC1D23",
            brand="Toyota",
            model="Corolla",
            year=2023,
            client_id="cli-123"
        )
        assert vehicle.license_plate == "ABC1D23"
        assert vehicle.brand == "Toyota"
        assert vehicle.model == "Corolla"
        assert vehicle.year == 2023
        assert vehicle.client_id == "cli-123"

    def test_vehicle_create_invalid_plate(self):
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="INVALID!",
                brand="Ford",
                model="Focus",
                year=2020,
                client_id=None
            )

    def test_vehicle_create_invalid_year(self):
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="ABC1D23",
                brand="Honda",
                model="Civic",
                year=1800,  # menor que 1886
                client_id=None
            )

    def test_vehicle_create_invalid_brand_model_length(self):
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="ABC1D23",
                brand="",  # vazio, min_length=1
                model="ModelX",
                year=2022
            )
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="ABC1D23",
                brand="BrandX",
                model="",  # vazio
                year=2022
            )

    def test_vehicle_update_requires_id(self):
        with pytest.raises(ValidationError):
            VehicleUpdate(
                license_plate="ABC1D23",
                brand="Toyota",
                model="Corolla",
                year=2023,
                client_id="cli-123"
            )
        vehicle = VehicleUpdate(
            id=1,
            license_plate="ABC1D23",
            brand="Toyota",
            model="Corolla",
            year=2023,
            client_id="cli-123"
        )
        assert vehicle.id == 1

    def test_vehicle_response_from_attributes(self):
        vehicle = VehicleResponse(
            id=1,
            license_plate="ABC1D23",
            brand="Toyota",
            model="Corolla",
            year=2023,
            client_id="cli-123"
        )
        assert vehicle.id == 1
        assert vehicle.license_plate == "ABC1D23"
