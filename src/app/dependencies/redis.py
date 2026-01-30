from redis.asyncio import Redis

async def get_redis() -> Redis:
    return Redis(host='redis')