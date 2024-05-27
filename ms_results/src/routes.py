from fastapi import FastAPI

from transport.handlers import answers


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        answers.router,
        prefix="/api/v1",
    )