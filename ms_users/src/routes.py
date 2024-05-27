from fastapi import FastAPI

from transport.handlers import users, auth


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        users.router,
        prefix="/api/v1/users",
    )
    
    app.include_router(
        auth.router,
        prefix="/api/v1/auth",
    )