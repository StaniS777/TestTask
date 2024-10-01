from fastapi import FastAPI

from src.routes.product import router as product_router
from src.routes.orders import router as order_router


app = FastAPI(
    title="Тестовое задание Станиславович А.Ю. (Разработка API для управления складом)"
)

app.include_router(product_router)
app.include_router(order_router)
