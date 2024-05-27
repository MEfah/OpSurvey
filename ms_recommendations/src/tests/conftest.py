import pytest_asyncio
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from integrations.db.session import get_session
from main import app
from settings import settings


@pytest_asyncio.fixture
async def session():
    """
    Фикстура сессии бд. Заменяет get_session в зависимостях
    Изменения, совершенные в рамках сессии не сохраняются
    """

    db_engine = create_async_engine(settings.database_url, echo=True, future=True)
    connection = await db_engine.connect()
    transaction = await connection.begin()

    async_session = AsyncSession(bind=connection)
    await async_session.begin_nested()

    app.dependency_overrides[get_session] = lambda: async_session

    yield async_session

    await async_session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client():
    """
    Клиент для осуществления запросов к мс
    """

    yield AsyncClient(app=app, base_url=settings.base_url)