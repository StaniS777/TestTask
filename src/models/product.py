from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal]
    quantity: Mapped[int]

    def __str__(self):
        return self.name
