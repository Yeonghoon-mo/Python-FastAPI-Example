import redis.asyncio as redis
from app.core.config import settings

# Redis Connection Pool
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    encoding="utf-8",
    decode_responses=True
)

# Redis Client
redis_client = redis.Redis(connection_pool=redis_pool)

async def get_redis_client():
    return redis_client

async def close_redis_connection():
    await redis_client.close()
