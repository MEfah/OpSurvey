from fastapi import FastAPI, Depends
from routes import setup_routes
from settings import settings
from services.tf_idf import initialize
# TODO: УБРАТЬ CORS
from fastapi.middleware.cors import CORSMiddleware
from exceptions import setup_exception_handlers
from contextlib import asynccontextmanager
from run_consumers import run_consumers
import nltk


def build_app() -> FastAPI:
    """Создание приложения FastAPI."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nltk.download('stopwords')
        await run_consumers()
        await initialize()
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app