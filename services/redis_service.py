from os import getenv

import redis.asyncio as redis


class RedisService:
    def redis():
        return redis.from_url(getenv("REDIS"), decode_responses=True)

    @classmethod
    async def set_with_expiry(cls, key: str, value: str, expiry: int) -> None:
        """Set a key-value pair in Redis with an expiration time."""
        await cls.redis().setex(key, expiry, value)

    @classmethod
    async def get(cls, key: str) -> str | None:
        """Get a value from Redis by key."""
        return await cls.redis().get(key)

    @classmethod
    async def delete(cls, key: str) -> None:
        """Delete a key from Redis."""
        await cls.redis().delete(key)
