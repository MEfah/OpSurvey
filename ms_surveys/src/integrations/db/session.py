from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import motor.motor_asyncio 
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
import pymongo

from settings import settings


client = motor.motor_asyncio.AsyncIOMotorClient(
        host = ["db_surveys:27017"],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "mongo",
        password = "mongo",)
db = client.get_database("surveys")


async def create_search_index():
    db.get_collection('surveys').create_index([
        ("name", pymongo.TEXT), 
        ("description", pymongo.TEXT)
    ])


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    """Получить коллекцию по названию. Не требует I/O, поэтому синхронный метод

    Yields:
        Any: MongoDB коллекция
    """
    
    return db[collection_name]