# src/infrastructure/redis/repository.py
from typing import Any
from redis.asyncio import Redis

from src.infrastructure.redis.client import get_redis_client


class RedisRepository:

    async def _get_client(self) -> Redis:
        return await get_redis_client()

    async def get(self, key: str) -> Any:
        redis = await self._get_client()
        return await redis.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        redis = await self._get_client()
        if ttl is not None:
            await redis.set(key, value, ex=ttl)
        else:
            await redis.set(key, value)

    async def delete(self, key: str) -> None:
        redis = await self._get_client()
        await redis.delete(key)

    async def exists(self, key: str) -> bool:
        redis = await self._get_client()
        return bool(await redis.exists(key))
