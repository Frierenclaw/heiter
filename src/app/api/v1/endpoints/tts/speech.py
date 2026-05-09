from typing import Annotated

from fastapi import APIRouter, Depends, Response

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.tts.schemas import TTSApiSpeechRequestDTO
from api.v1.steosvoice import SteosVoice
from models.user import User

speech_api_router = APIRouter()


@speech_api_router.post('/speech')
async def speech_endpoint(
    dto: TTSApiSpeechRequestDTO, 
    user: Annotated[User, Depends(get_current_user)]
):
    audio_bytes = await SteosVoice.synthesis_by_text(
        input_text=dto.input,
        speed=dto.speed
    )

    return Response(
        content=audio_bytes, 
        media_type="audio/mpeg" 
    )