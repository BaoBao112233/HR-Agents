import redis.asyncio as redis
import json
import os
from typing import Any, Optional

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Redis client (will be initialized on first use)
_redis_client: Optional[redis.Redis] = None

async def get_redis_client() -> redis.Redis:
    """Get or create Redis client"""
    global _redis_client
    if _redis_client is None:
        _redis_client = await redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client

async def close_redis_client():
    """Close Redis client"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None

# Cache operations
async def cache_set(key: str, value: Any, expiry: int = 3600):
    """Set a value in cache with expiry (default 1 hour)"""
    client = await get_redis_client()
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    await client.setex(key, expiry, value)

async def cache_get(key: str) -> Optional[Any]:
    """Get a value from cache"""
    client = await get_redis_client()
    value = await client.get(key)
    if value:
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return None

async def cache_delete(key: str):
    """Delete a key from cache"""
    client = await get_redis_client()
    await client.delete(key)

async def cache_exists(key: str) -> bool:
    """Check if key exists in cache"""
    client = await get_redis_client()
    return await client.exists(key) > 0

# Agent memory operations
async def store_agent_memory(agent_id: str, conversation: list, expiry: int = 7200):
    """Store agent conversation memory (default 2 hours)"""
    key = f"agent_memory:{agent_id}"
    await cache_set(key, conversation, expiry)

async def get_agent_memory(agent_id: str) -> Optional[list]:
    """Get agent conversation memory"""
    key = f"agent_memory:{agent_id}"
    return await cache_get(key)

async def clear_agent_memory(agent_id: str):
    """Clear agent memory"""
    key = f"agent_memory:{agent_id}"
    await cache_delete(key)

# Session caching
async def cache_session_data(session_id: str, data: dict, expiry: int = 3600):
    """Cache session data"""
    key = f"session:{session_id}"
    await cache_set(key, data, expiry)

async def get_session_data(session_id: str) -> Optional[dict]:
    """Get session data"""
    key = f"session:{session_id}"
    return await cache_get(key)

# Result caching
async def cache_candidate_extraction(file_hash: str, data: dict, expiry: int = 86400):
    """Cache extracted candidate data (24 hours)"""
    key = f"extraction:{file_hash}"
    await cache_set(key, data, expiry)

async def get_cached_extraction(file_hash: str) -> Optional[dict]:
    """Get cached extraction"""
    key = f"extraction:{file_hash}"
    return await cache_get(key)

async def cache_score_result(candidate_id: str, jd_id: str, score_data: dict, expiry: int = 3600):
    """Cache score result"""
    key = f"score:{candidate_id}:{jd_id}"
    await cache_set(key, score_data, expiry)

async def get_cached_score(candidate_id: str, jd_id: str) -> Optional[dict]:
    """Get cached score"""
    key = f"score:{candidate_id}:{jd_id}"
    return await cache_get(key)

# Analytics caching
async def cache_analytics(key: str, data: Any, expiry: int = 600):
    """Cache analytics data (10 minutes)"""
    cache_key = f"analytics:{key}"
    await cache_set(cache_key, data, expiry)

async def get_cached_analytics(key: str) -> Optional[Any]:
    """Get cached analytics"""
    cache_key = f"analytics:{key}"
    return await cache_get(key)

# Utility functions
async def increment_counter(key: str, amount: int = 1) -> int:
    """Increment a counter"""
    client = await get_redis_client()
    return await client.incrby(key, amount)

async def get_counter(key: str) -> int:
    """Get counter value"""
    client = await get_redis_client()
    value = await client.get(key)
    return int(value) if value else 0
