from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.user import User
from redis_db import RedisClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme())]):
    user_id = await RedisClient.check_token(token=token)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Bad token')
    
    user = await User.get_or_none(id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    
    return user