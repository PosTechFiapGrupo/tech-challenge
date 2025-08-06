from dataclasses import dataclass

@dataclass
class InventoryItem:
    id: int | None
    name: str
    description: str
    quantity: int
    minimum_stock: int
    unit_price: float
