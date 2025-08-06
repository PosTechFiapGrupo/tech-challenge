from pydantic import BaseModel, Field

class InventoryItemCreate(BaseModel):
    name: str = Field(..., example="Óleo de motor")
    description: str = Field(..., example="Lubrificante 5W30")
    quantity: int = Field(..., example=10)
    minimum_stock: int = Field(..., example=3)
    unit_price: float = Field(..., example=89.90)

class InventoryItemUpdate(InventoryItemCreate):
    pass

class InventoryItemOut(InventoryItemCreate):
    id: int

    class Config:
        from_attributes = True
