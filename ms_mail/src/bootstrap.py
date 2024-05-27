from fastapi import FastAPI
# TODO: УБРАТЬ CORS
from fastapi.middleware.cors import CORSMiddleware
#from exceptions import setup_exception_handlers
from routes import setup_routes
from settings import settings
from exceptions import setup_exception_handlers


def build_app() -> FastAPI:
    """Создание приложения FastAPI."""

    app_params = {
        "debug": settings.debug,
        "title": settings.project.title,
        "description": settings.project.description,
        "version": settings.project.version
    }
    app = FastAPI(**app_params)

    setup_routes(app)
    setup_exception_handlers(app)
    # TODO убрать
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app