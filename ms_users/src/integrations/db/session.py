from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)


async def get_session() -> AsyncGenerator:
    """Получить сессию для взаимодействия с базой данных

    Yields:
        Iterator[AsyncGenerator]: Сессия бд
    """

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        
        