from src.repositories.product import ProductRepository
from src.schemas.product import (
    ProductCreateSchema,
    ProductRetrieveSchema,
    ProductUpdateSchema,
)
from src.services.base import BaseService


class ProductService(
    BaseService[
        ProductRepository,
        ProductRetrieveSchema,
        ProductCreateSchema,
        ProductUpdateSchema,
    ]
):
    retrieve_schema = ProductRetrieveSchema
    create_schema = ProductCreateSchema
    update_schema = ProductUpdateSchema
