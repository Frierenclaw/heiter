import json
from uuid import UUID

from core.clients import redis_client


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
    
    @staticmethod
    async def get_context(user_id: str):
        context = await redis_client.lrange(
            name=f'context:{user_id}',
            start=0,
            end=-1
        )
        serialized_messages = [json.loads(message) for message in context]

        return serialized_messages
    
    @staticmethod
    async def put_in_context(user_id: str,
                             messages: list[dict]):
        messages = [json.dumps(message) for message in messages]

        context = await redis_client.lpush(
            f'context:{user_id}',
            *messages
        )
    