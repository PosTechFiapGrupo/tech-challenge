from pydantic import BaseModel

class InventoryItemBase(BaseModel):
    name: str
    description: str
    quantity: int

    model_config = {
        "from_attributes": True
    }
class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int