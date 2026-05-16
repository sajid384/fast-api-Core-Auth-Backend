import redis.asyncio as redis

REDIS_URL = "redis://localhost:6379"

def get_redis():
    return redis.from_url(
        REDIS_URL,
        decode_responses=True
    )

async def add_to_blacklist(token: str):

    redis_client = get_redis()

    await redis_client.set(
        token,
        "blacklisted",
        ex=3600
    )

    await redis_client.close()


async def is_blacklisted(token: str):

    redis_client = get_redis()

    result = await redis_client.get(token)

    await redis_client.close()

    return result is not None