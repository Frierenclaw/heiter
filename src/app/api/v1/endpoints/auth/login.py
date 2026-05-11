from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from api.v1.auth_logic import Auth
from api.v1.endpoints.auth.schemas import LoginResponseDTO
from models.user import User

router = APIRouter()

@router.post('/login', response_model=LoginResponseDTO)
async def login_endpoint(user_dto: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate a user and return an access token.

    The endpoint accepts OAuth2 password form data, validates the user
    credentials, generates a JWT access token, and stores the token in the
    whitelist for future verification.

    Args:
        user_dto (Annotated[OAuth2PasswordRequestForm, Depends()]): OAuth2 password request form.

    Raises:
        HTTPException: If the username does not exist.
        HTTPException: If the password is invalid.
        HTTPException: If an error occurs while checking the password hash.
        HTTPException: If an error occurs while generating or whitelisting the token.

    Returns:
        LoginResponseDTO: The response containing the generated access token.
    """
    
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