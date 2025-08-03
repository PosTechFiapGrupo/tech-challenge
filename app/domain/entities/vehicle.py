from dataclasses import dataclass

@dataclass
class Vehicle:
    id: int
    license_plate: str
    brand: str
    model: str
    year: int
