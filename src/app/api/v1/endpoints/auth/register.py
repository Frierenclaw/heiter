from fastapi import APIRouter, HTTPException, status
from loguru import logger

from api.v1.auth_logic import Auth
from api.v1.endpoints.auth.schemas import RegisterRequestDTO
from models.user import User

router = APIRouter()

@router.post('/register')
async def register_account(dto: RegisterRequestDTO):
    """Register a new user and return an authentication token.

    Args:
        dto (RegisterRequestDTO): User registration data containing username and password.

    Raises:
        HTTPException: If password hashing or user creation fails.

    Returns:
        dict: A response object with 'created' status and optional 'token'.
    """
    
    try:
        hashed_password = Auth.hash_password(dto.password)
    except Exception as e:
        logger.error(f'Error while hashing password for new user {dto.username}. Detail: {e} ')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
            detail='Unexcepted error. Please try again')

    try:
        user = await User.create(
            username=dto.username,
            password=hashed_password)
        
        try:
            token = Auth.generate_token()
            await Auth.whitelist_token(token,
                                       user.id)
            
            return {
                'created': True,
                'token': token
            }
        except Exception as e:
            logger.error(f'Error while generating token for user id={user.id}. Error: {e}')
            
            return {'created': True,
                    'token': None}
    except Exception as e:
        logger.error(f'Unexcepted error for new user {dto.username}. Detail: {e} ')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
            detail='Unexcepted error. Please try again')