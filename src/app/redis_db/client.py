from uuid import UUID

from core.config import redis_client


class RedisClient:
    @staticmethod
    async def put_token(token: str,
                        user_id: UUID,
                        alive_seconds: int): # secrets.token_urlsafe
        result = await redis_client.set(name=f'token:{token}',
                               value=str(user_id),
                               ex=alive_seconds)
        
        return result
    
    @staticmethod
    async def check_token(token: str):
        token_value = await redis_client.get(
            name=f'token:{token}'
        )

        return token_value