import pytest
from app.domain.entities.vehicle import Vehicle


class TestVehicleEntity:

    def test_create_vehicle_with_all_fields(self):
        vehicle = Vehicle(
            id=1,
            license_plate="ABC1D23",
            model="Onix",
            brand="Chevrolet",
            year=2020
        )

        assert vehicle.id == 1
        assert vehicle.license_plate == "ABC1D23"
        assert vehicle.model == "Onix"
        assert vehicle.brand == "Chevrolet"
        assert vehicle.year == 2020

    def test_create_vehicle_without_id(self):
        vehicle = Vehicle(
            license_plate="XYZ9A88",
            model="Civic",
            brand="Honda",
            year=2021
        )

        assert vehicle.id is None
        assert vehicle.license_plate == "XYZ9A88"
        assert vehicle.model == "Civic"
        assert vehicle.brand == "Honda"
        assert vehicle.year == 2021

    def test_vehicle_field_types(self):
        vehicle = Vehicle(
            id=10,
            license_plate="DEF2G34",
            model="Corolla",
            brand="Toyota",
            year=2019
        )

        assert isinstance(vehicle.id, int)
        assert isinstance(vehicle.license_plate, str)
        assert isinstance(vehicle.model, str)
        assert isinstance(vehicle.brand, str)
        assert isinstance(vehicle.year, int)