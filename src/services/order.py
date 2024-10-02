from uuid import UUID
from asyncpg import DataError
from sqlalchemy.exc import ProgrammingError


from src.models.order import OrderStatus
from src.repositories.order import OrderRepository, OrderItemRepository
from src.schemas.order import (
    OrderRetrieveSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderAddItemsSchema,
    OrderItemCreateSchema,
    OrderRetrieveListSchema,
)
from src.schemas.product import ProductUpdateSchema
from src.services.product import ProductService
from src.services.base import BaseService


class OrderService(
    BaseService[
        OrderRepository,
        OrderRetrieveListSchema,
        OrderAddItemsSchema,
        OrderUpdateSchema,
    ]
):
    retrieve_schema = OrderRetrieveListSchema
    create_schema = OrderAddItemsSchema
    update_schema = OrderUpdateSchema

    def __init__(
        self,
        order_item_repo: "OrderItemRepository",
        product_service: "ProductService",
        *args,
        **kwargs
    ):
        self.order_item_repo = order_item_repo
        self.product_service = product_service
        super().__init__(*args, **kwargs)

    async def get_products_quantity(self, product_uuids: list[str | UUID]):
        products = await self.product_service.get_list_by_ids(product_uuids)
        result = {product.pk: product.quantity for product in products}
        return result

    async def create(self, data: OrderAddItemsSchema) -> OrderRetrieveSchema:
        order_items = data.items
        product_uuids = [order_item.product_uuid for order_item in order_items]
        product_quantity_map = await self.get_products_quantity(product_uuids)

        for item in order_items:
            quantity_warehouse = product_quantity_map.get(item.product_uuid)
            if quantity_warehouse is None:
                raise ProgrammingError("Product does not exist")

            col = quantity_warehouse - item.quantity
            if col < 0:
                raise DataError("Wrong product quantity")

            product_quantity_map[item.product_uuid] = col

        order = await self.repo.create_one(OrderCreateSchema.model_validate(data).model_dump())

        for item in order_items:
            order_item_data = OrderItemCreateSchema(
                order_uuid=order.pk,
                product_uuid=item.product_uuid,
                quantity=item.quantity,
            )
            await self.order_item_repo.create_one(order_item_data.model_dump())

        for product_uuid, product_quantity in product_quantity_map.items():
            product_update_data = ProductUpdateSchema(quantity=product_quantity)
            await self.product_service.update(product_uuid, product_update_data)

        return OrderRetrieveSchema.model_validate(order)
    
    async def update(self, obj_id: str | UUID, data: OrderUpdateSchema, partial=True) -> OrderRetrieveSchema:
        order = await self.repo.update_one(
            obj_id, data.model_dump(exclude_unset=partial)
        )
        return OrderRetrieveSchema.model_validate(order)

    async def update_status(self, order_id: UUID, status: OrderStatus) -> OrderRetrieveSchema:
        order = await self.repo.update_one(
            order_id, {"status": status}
        )
        return OrderRetrieveSchema.model_validate(order)
