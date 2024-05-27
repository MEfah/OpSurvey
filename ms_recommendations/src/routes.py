from fastapi import FastAPI

from transport.handlers import recommendations


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        recommendations.router,
        prefix="/api/v1/recommendations",
    )