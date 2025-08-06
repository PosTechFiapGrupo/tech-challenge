from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.infrastructure.schemas.inventory_item_schema import InventoryItemCreate, InventoryItemOut, InventoryItemUpdate
from app.domain.use_cases.inventory_item_use_case import InventoryItemUseCase

router = APIRouter(prefix="/inventory", tags=["Inventory Items"])

@router.get("/", response_model=List[InventoryItemOut])
@inject
async def list_items(
    use_case: InventoryItemUseCase = Depends(Provide[Container.inventory_item_use_case])
):
    return await use_case.list_items()

@router.get("/{item_id}", response_model=InventoryItemOut)
@inject
async def get_item(
    item_id: int,
    use_case: InventoryItemUseCase = Depends(Provide[Container.inventory_item_use_case])
):
    return await use_case.get_item(item_id)

@router.post("/", response_model=InventoryItemOut, status_code=201)
@inject
async def create_item(
    item: InventoryItemCreate,
    use_case: InventoryItemUseCase = Depends(Provide[Container.inventory_item_use_case])
):
    return await use_case.create_item(item)

@router.put("/{item_id}", response_model=InventoryItemOut)
@inject
async def update_item(
    item_id: int,
    item: InventoryItemUpdate,
    use_case: InventoryItemUseCase = Depends(Provide[Container.inventory_item_use_case])
):
    return await use_case.update_item(item_id, item)

@router.delete("/{item_id}", status_code=204)
@inject
async def delete_item(
    item_id: int,
    use_case: InventoryItemUseCase = Depends(Provide[Container.inventory_item_use_case])
):
    await use_case.delete_item(item_id)
