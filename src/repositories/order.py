from src.repositories.base import BaseRepository

from src.models.order import Order, OrderItem


class OrderRepository(BaseRepository[Order]):
    model = Order


class OrderItemRepository(BaseRepository[OrderItem]):
    model = OrderItem
