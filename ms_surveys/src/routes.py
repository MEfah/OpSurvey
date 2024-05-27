from fastapi import FastAPI

from transport.handlers import surveys, users_surveys, unfinished


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        surveys.router,
        prefix="/api/v1/surveys",
    )
    
    app.include_router(
        users_surveys.router,
        prefix="/api/v1/users",
    )
    
    app.include_router(
        unfinished.router,
        prefix="/api/v1/unfinished",
    )