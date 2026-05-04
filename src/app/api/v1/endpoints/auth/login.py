from fastapi import APIRouter, HTTPException, status
from loguru import logger

from api.v1.auth_logic import Auth
from api.v1.endpoints.auth.schemas import LoginRequestDTO, LoginResponseDTO
from models.user import User

router = APIRouter()

@router.post('/login', response_model=LoginResponseDTO)
async def login_endpoint(user_dto: LoginRequestDTO):
    user = await User.get_or_none(username=user_dto.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        password_is_valid = Auth.check_password(password=user_dto.password,
                                                hashed_password=user.password)
    except Exception as e:
        logger.error(f'Error while checking password hash. Username: {user_dto.username}, error: {e}')
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
                            detail='Server-side error. Try again in few minutes')
    
    if not password_is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = Auth.generate_token()
        await Auth.whitelist_token(token=token,
                                   user_id=user.id)
        
    except Exception as e:
        logger.error(f'Error while generating access token. Username: {user_dto.username}, error: {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
                            detail='Server-side error. Try again in few minutes')
    
    response = LoginResponseDTO(access_token=token)

    return response