from app.core.database import AsyncSessionLocal
from app.core.redis import redis_client


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_redis():
    return redis_client