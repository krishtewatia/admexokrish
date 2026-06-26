"""Motor (async MongoDB) client."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
from loguru import logger

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)
        _db = _client[settings.mongodb_db_name]
        logger.info(f"Connected to DB: {settings.mongodb_db_name}")
    return _db


async def create_indexes():
    db = get_db()
    await db["leads"].create_index("email", unique=True)
    await db["leads"].create_index([("submittedAt", -1)])
    logger.info("Indexes created")


async def close_client():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
