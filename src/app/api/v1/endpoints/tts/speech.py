from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.tts.schemas import TTSApiSpeechRequestDTO
from models.user import User

speech_api_router = APIRouter()


@speech_api_router.post('/speech')
async def speech_endpoint(
    dto: TTSApiSpeechRequestDTO, 
    user: Annotated[User, Depends(get_current_user)]
):
    pass
