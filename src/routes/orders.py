from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_order_service
from src.services.order import OrderService

from src.schemas.order import (
    OrderAddItemsSchema, 
    OrderRetrieveListSchema, 
    OrderRetrieveSchema, 
    OrderUpdateStatusSchema
)


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("")
async def order_create(
    data: OrderAddItemsSchema,
    service: OrderService = Depends(get_order_service),
):
    result = await service.create(data)
    return result

@router.get("/")
async def order_list(
    service: OrderService = Depends(get_order_service),
) -> list[OrderRetrieveListSchema]:
    result = await service.get_all()
    return result

@router.get("/orders/{order_id}", response_model=OrderRetrieveListSchema)
async def get_order_by_id(
    order_id: UUID, 
    service: OrderService = Depends(get_order_service),
) -> OrderRetrieveSchema:
    
    result = await service.get_one_by_id(order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return result

@router.patch("/{order_id}/status", response_model=OrderRetrieveListSchema)    
async def patch_order_by_id(
    order_id: UUID,
    data: OrderUpdateStatusSchema,
    service: OrderService = Depends(get_order_service),
) -> OrderRetrieveSchema: 
    
    result = await service.update_status(order_id, data.status  )
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return result
