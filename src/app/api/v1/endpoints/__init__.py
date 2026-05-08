from fastapi import APIRouter

from api.v1.endpoints.auth import base_auth_router
from api.v1.endpoints.gpt.create_completions import chat_completions_router
from api.v1.endpoints.tts import base_tts_router

base_api_router = APIRouter(prefix='/v1')
base_api_router.include_router(chat_completions_router)
base_api_router.include_router(base_auth_router)
base_api_router.include_router(base_tts_router)