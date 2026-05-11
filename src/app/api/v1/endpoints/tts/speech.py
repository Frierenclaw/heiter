from typing import Annotated

from fastapi import APIRouter, Depends, Response

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.tts.schemas import TTSApiSpeechRequestDTO
from api.v1.steosvoice import SteosVoice
from core.config import config
from models.user import User

speech_api_router = APIRouter()


@speech_api_router.post('/speech')
async def speech_endpoint(
    dto: TTSApiSpeechRequestDTO, 
    user: Annotated[User, Depends(get_current_user)]
):
    """
    Synthesizes speech from the provided text and returns the audio.

    Args:
        dto (TTSApiSpeechRequestDTO): The request data containing input text and speed.

    Returns:
        Response: The synthesized audio as an MP3 response.
    """
    audio_bytes = await SteosVoice.synthesis_by_text(
        input_text=dto.input,
        speed=dto.speed,
        steos_token=config.STEOS_TOKEN
    )

    return Response(
        content=audio_bytes, 
        media_type="audio/mpeg" 
    )