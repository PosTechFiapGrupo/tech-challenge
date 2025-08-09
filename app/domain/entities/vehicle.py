from typing import Optional
from dataclasses import dataclass

@dataclass
class Vehicle:
    license_plate: str
    brand: str
    model: str
    year: int
    client_id: Optional[str] = None
    id: Optional[int] = None