from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import motor.motor_asyncio 
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
import pymongo

from settings import settings


client = motor.motor_asyncio.AsyncIOMotorClient(
        host = ["db_results:27017"],
        serverSelectionTimeoutMS = 3000,
        username = "mongo",
        password = "mongo",)
db = client.get_database("results")


async def create_index():
    await db.get_collection('answers').create_index([("survey_id", 1), ("user_id", 1)], unique=True)


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    """Получить коллекцию по названию. Не требует I/O, поэтому синхронный метод

    Yields:
        Any: MongoDB коллекция
    """
    
    return db[collection_name]