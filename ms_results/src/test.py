from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import motor.motor_asyncio 
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from services.pipelines.results import get_result_pipeline
import pymongo
import asyncio
from settings import settings


client = motor.motor_asyncio.AsyncIOMotorClient(
        host = ["localhost:27017"],
        serverSelectionTimeoutMS = 3000,
        username = "mongo",
        password = "mongo",)
db = client.get_database("results")


async def main():
    print(await db.get_collection('answers').aggregate(get_result_pipeline('664cdecf277fa6b17c6402c8')).to_list(100))


if __name__ == '__main__':
    asyncio.run(main())