from fastapi import APIRouter

from api.v1.endpoints.tts import speech

base_tts_router = APIRouter(prefix='/audio')
base_tts_router.include_router(speech.speech_api_router,
    tags=['Speech'])
