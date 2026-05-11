from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse

from api.v1.dependencies.auth import get_current_user
from api.v1.edgetts import EdgeTTS
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

    async def generate_audio():
        if dto.model == 'edge_tts':
            audio_source = await EdgeTTS.synthesis_by_text(input_text=dto.input, voice=dto.voice)
        elif dto.model == 'steosvoice':
            audio_source = await SteosVoice.synthesis_by_text(
                input_text=dto.input, 
                speed=dto.speed, 
                steos_token=config.STEOS_TOKEN
            )
        
        async for chunk in audio_source.stream():
            if isinstance(chunk, dict) and chunk.get("type") == "audio":
                yield chunk["data"]
            elif isinstance(chunk, bytes):
                yield chunk

    # Возвращаем специальный объект ответа
    return StreamingResponse(generate_audio(), media_type='audio/mpeg')