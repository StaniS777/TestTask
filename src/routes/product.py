from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.services.product import ProductService

from src.schemas.product import (
    ProductCreateSchema,
    ProductOneSchema,
    ProductRetrieveSchema,
    ProductUpdateSchema,
)

from src.dependencies import get_product_service


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def product_list(
    service: ProductService = Depends(get_product_service),
) -> list[ProductRetrieveSchema]:
    result = await service.get_all()
    return result


@router.post("/")
async def product_create(
    data: ProductCreateSchema,
    service: ProductService = Depends(get_product_service),
) -> ProductRetrieveSchema:
    result = await service.create(data)
    return result

@router.get("/{product_id}", response_model=ProductRetrieveSchema)    
async def get_product_id(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
) -> ProductRetrieveSchema:
    
    result = await service.get_one_by_id(product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return result

@router.put("/{product_id}", response_model=ProductRetrieveSchema)    
async def put_product_id(
    product_id: UUID,
    data: ProductUpdateSchema,
    service: ProductService = Depends(get_product_service),
) -> ProductRetrieveSchema:
    
    result = await service.update(product_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return result

@router.delete("/{product_id}")    
async def delete_product_id(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):
    await service.delete(product_id)
   
    return HTTPException(status_code=200)
