from typing import Any, Optional
import json
import redis.asyncio as redis
from config.settings import get_settings

settings = get_settings()

class RedisStore:
    def __init__(self):
        # Build Redis connection kwargs
        redis_kwargs = {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "db": settings.REDIS_DB,
            "decode_responses": True
        }
        
        # Only add password if configured
        if settings.REDIS_PASSWORD:
            redis_kwargs["password"] = settings.REDIS_PASSWORD
        
        self.redis = redis.Redis(**redis_kwargs)
    
    async def initialize(self) -> None:
        """Test Redis connection and create required keys"""
        try:
            await self.redis.ping()
        except Exception as e:
            raise Exception(f"Redis connection error: {str(e)}")
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            serialized = json.dumps(value)
            # Updated method signature to match Redis client API
            await self.redis.set(name=key, value=serialized, ex=ttl)
            return True
        except Exception as e:
            raise Exception(f"Redis set error: {str(e)}")
    
    async def get(self, key: str) -> Optional[Any]:
        try:
            # Updated method signature to match Redis client API
            value = await self.redis.get(name=key)
            return json.loads(value) if value else None
        except Exception as e:
            raise Exception(f"Redis get error: {str(e)}")
    
    async def delete(self, key: str) -> bool:
        try:
            # Updated method signature to match Redis client API
            return bool(await self.redis.delete(key))
        except Exception as e:
            raise Exception(f"Redis delete error: {str(e)}")
