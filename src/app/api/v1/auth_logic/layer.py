import secrets
from uuid import UUID

import bcrypt

from redis_db import RedisClient


class Auth:

    @staticmethod
    def hash_password(password: str,
                      salt_rounds: int = 12) -> bytes:
        
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed_password = bcrypt.hashpw(password=password.encode('utf-8'),
                                        salt=salt)
        
        return hashed_password
    
    @staticmethod
    def check_password(password: str,
                       hashed_password: bytes) -> bool:
        password = password.encode('utf-8')
        
        password_is_valid = bcrypt.checkpw(
            password=password,
            hashed_password=hashed_password
        )

        return password_is_valid
    
    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(nbytes=32)
    
    @staticmethod
    async def whitelist_token(token: str,
                              user_id: UUID):
        status = await RedisClient.put_token(token=token,
                                    user_id=user_id)
        
        return status