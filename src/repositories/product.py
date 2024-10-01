from src.repositories.base import BaseRepository

from src.models import Product


class ProductRepository(BaseRepository[Product]):
    model = Product
