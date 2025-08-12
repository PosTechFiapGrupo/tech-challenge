from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class InventoryMovement:
    id: int
    item_id: int
    type: str
    quantity: int
    os_id: Optional[str]
    note: Optional[str]
    created_at: datetime
