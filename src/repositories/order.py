from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.order import Order, OrderItem


class OrderRepository(BaseRepository[Order]):
    model = Order

    @property
    def default_select_query(self):
        stmt = (
            select(self.model).
            options(selectinload(self.model.items))
        )
        return stmt


class OrderItemRepository(BaseRepository[OrderItem]):
    model = OrderItem
