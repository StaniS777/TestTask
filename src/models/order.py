from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class OrderStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    SENT = "sent"
    DELIVERED = "delivered"


class Order(Base):
    __tablename__ = "orders"

    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.IN_PROGRESS)
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    product_uuid: Mapped[UUID] = mapped_column(ForeignKey("products.pk"))
    order_uuid: Mapped[UUID] = mapped_column(ForeignKey("orders.pk"))
    quantity: Mapped[int]
    order: Mapped["Order"] = relationship("Order", back_populates="items")
