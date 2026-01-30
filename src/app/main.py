import logging

from fastapi import FastAPI
from app.routers.docs import router
from app.api import healthz
from prometheus_client import make_asgi_app
from app.monitoring.middleware import prometheus_middleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = FastAPI(
        description="""
# Демо-приложение
В данном приложении можно проверить корректность считанных паспортных данных
"""
)

app.middleware('http')(prometheus_middleware)
metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)

app.include_router(router)
@app.get("/", tags=["root"])
def root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение и ссылки на документацию.
    """
    return {
        "message": "Добро пожаловать в User Service API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }

app.include_router(healthz.router)
