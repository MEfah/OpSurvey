from fastapi import FastAPI
from transport.handlers import email

def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        email.router,
        prefix="/api/v1",
    )