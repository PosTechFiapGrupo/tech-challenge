from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EntryRequest(BaseModel):
    quantity: int = Field(gt=0)
    note: Optional[str] = None

class ConsumeItem(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)

class ConsumeRequest(BaseModel):
    os_id: str
    items: List[ConsumeItem]

class MovementOut(BaseModel):
    id: int
    item_id: int
    os_id: Optional[str] = None
    type: str
    quantity: int
    note: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
