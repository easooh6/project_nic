import redis.asyncio as redis
from src.infrastructure.settings.settings import settings

_redis_client = None

async def init_redis_client():
    global _redis_client
    if _redis_client is None:

        _redis_client = redis.from_url(
            url=settings.redis.REDIS_URL, 
            decode_responses=True,
            max_connections=10
        )
    try:
        await _redis_client.ping()
    except Exception as e:
        raise e
    
    return _redis_client

async def close_redis_client():
    if _redis_client:
        await _redis_client.close()

async def get_redis_client():
    if _redis_client is None:
        raise RuntimeError("Redis client is not initialized")
    return _redis_client