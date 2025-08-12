from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.infrastructure.schemas.inventory_stock_schema import (
    EntryRequest, ConsumeRequest, MovementOut
)
from app.domain.use_cases.inventory_stock_use_case import InventoryStockUseCase
from app.infrastructure.auth_dependencies import role_required

router = APIRouter(prefix="/inventory", tags=["Inventory Stock"])

@router.post("/{item_id}/entries", status_code=204,
             dependencies=[Depends(role_required("admin", "atendente"))])
@inject
async def add_entry(
    item_id: int,
    payload: EntryRequest,
    use_case: InventoryStockUseCase = Depends(Provide[Container.inventory_stock_use_case]),
):
    await use_case.entrada(item_id, payload.quantity, payload.note)

@router.post("/consume", status_code=204,
             dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def consume_stock(
    payload: ConsumeRequest,
    use_case: InventoryStockUseCase = Depends(Provide[Container.inventory_stock_use_case]),
):
    try:
        items = [i.model_dump() for i in payload.items]  # [{item_id, quantity}]
        await use_case.consumir_para_os(payload.os_id, items)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))

@router.get("/{item_id}/movements", response_model=List[MovementOut],
            dependencies=[Depends(role_required("admin", "atendente", "mecanico"))])
@inject
async def list_movements(
    item_id: int,
    use_case: InventoryStockUseCase = Depends(Provide[Container.inventory_stock_use_case]),
):
    return await use_case.listar_movimentos(item_id)
