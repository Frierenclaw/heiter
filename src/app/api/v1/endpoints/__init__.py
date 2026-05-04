from fastapi import APIRouter

from api.v1.endpoints.gpt.create_completions import chat_completions_router

base_api_router = APIRouter(prefix='/v1')
base_api_router.include_router(chat_completions_router)