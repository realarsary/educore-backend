from app.core.redis import redis_client


async def get_stored_refresh(user_id: str):
    return await redis_client.get(f"refresh:{user_id}")


async def save_refresh(user_id: str, token: str):
    await redis_client.set(
        f"refresh:{user_id}",
        token,
        ex=60 * 60 * 24 * 7,
    )


async def delete_refresh(user_id: str):
    await redis_client.delete(f"refresh:{user_id}")