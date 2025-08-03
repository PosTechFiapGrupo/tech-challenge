from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import database
from app.infrastructure.repositories.inventory_item_repository_impl import InventoryItemRepositoryImpl
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase
from app.domain.entities.inventory_item import InventoryItem
from app.infrastructure.schemas.inventory_item_schema import (
    InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
)

router = APIRouter(prefix="/inventory_items", tags=["inventory_items"])

# Async generator para injetar a sessão async no FastAPI
async def get_db_session() -> AsyncSession:
    async for session in database.get_session():
        yield session

def get_use_case(db: AsyncSession = Depends(get_db_session)) -> InventoryItemUseCase:
    repo = InventoryItemRepositoryImpl(db)
    return InventoryItemUseCase(repo)

@router.post("/", response_model=InventoryItemResponse)
async def create_item(data: InventoryItemCreate, use_case: InventoryItemUseCase = Depends(get_use_case)):
    item = InventoryItem(id=0, **data.dict())
    return await use_case.create(item)

@router.get("/", response_model=list[InventoryItemResponse])
async def list_items(use_case: InventoryItemUseCase = Depends(get_use_case)):
    return await use_case.list_all()

@router.get("/{item_id}", response_model=InventoryItemResponse)
async def get_item(item_id: int, use_case: InventoryItemUseCase = Depends(get_use_case)):
    item = await use_case.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=InventoryItemResponse)
async def update_item(item_id: int, data: InventoryItemUpdate, use_case: InventoryItemUseCase = Depends(get_use_case)):
    item = InventoryItem(id=item_id, **data.dict())
    result = await use_case.update(item)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, use_case: InventoryItemUseCase = Depends(get_use_case)):
    await use_case.delete(item_id)
