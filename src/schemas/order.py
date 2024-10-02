from datetime import datetime
from uuid import UUID

from src.schemas.base import BaseModel
from src.models.order import OrderStatus



class OrderItemAddSchema(BaseModel):
    product_uuid: UUID
    quantity: int


class OrderRetrieveSchema(BaseModel):
    pk: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class OrderCreateSchema(BaseModel):
    pass


class OrderAddItemsSchema(BaseModel):
    items: list[OrderItemAddSchema]


class OrderUpdateSchema(BaseModel):
    status: OrderStatus


class OrderUpdateStatusSchema(BaseModel):
    status: OrderStatus


class OrderItemRetrieveSchema(BaseModel):
    pk: UUID
    product_uuid: UUID
    order_uuid: UUID
    quantity: int


class OrderItemCreateSchema(BaseModel):
    product_uuid: UUID
    order_uuid: UUID
    quantity: int


class OrderItemUpdateSchema(BaseModel):
    product_uuid: UUID = None
    order_uuid: UUID = None
    quantity: int = None


class OrderRetrieveListSchema(BaseModel):
    pk: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemAddSchema] = None
