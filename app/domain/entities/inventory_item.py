from dataclasses import dataclass

@dataclass
class InventoryItem:
    id: int
    name: str
    description: str
    quantity: int