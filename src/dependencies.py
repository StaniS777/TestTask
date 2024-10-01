from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.order import OrderItemRepository, OrderRepository
from src.repositories.product import ProductRepository

from src.database import get_async_session

from src.services.order import OrderService
from src.services.product import ProductService


def get_product_service(session: AsyncSession = Depends(get_async_session)):
    repo = ProductRepository(session)
    service = ProductService(repo)
    return service


def get_order_service(session: AsyncSession = Depends(get_async_session)):
    repo = OrderRepository(session)
    order_item_repo = OrderItemRepository(session)
    product_repo = ProductRepository(session)
    product_service = ProductService(product_repo)
    service = OrderService(order_item_repo, product_service, repo)
    return service
