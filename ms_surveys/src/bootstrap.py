from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
# TODO: УБРАТЬ CORS
from fastapi.middleware.cors import CORSMiddleware
#from exceptions import setup_exception_handlers
from routes import setup_routes
from settings import settings
from integrations.db.session import create_search_index
from run_consumers import run_consumers
from exceptions import setup_exception_handlers


def build_app() -> FastAPI:
    """Создание приложения FastAPI."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await create_search_index()
        await run_consumers()
        yield

    app_params = {
        "debug": settings.debug,
        "title": settings.project.title,
        "description": settings.project.description,
        "version": settings.project.version,
        "lifespan": lifespan
    }
    app = FastAPI(**app_params)

    setup_routes(app)
    setup_exception_handlers(app)
    app.mount("/media/surveys", StaticFiles(directory="/media/surveys"), name="media")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app