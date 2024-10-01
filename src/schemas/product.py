from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.schemas.base import BaseModel


class ProductRetrieveSchema(BaseModel):
    pk: UUID
    name: str
    description: str
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: Decimal
    quantity: int


class ProductUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    price: Decimal = None
    quantity: int = None


class ProductOneSchema(BaseModel):
    pk: UUID
