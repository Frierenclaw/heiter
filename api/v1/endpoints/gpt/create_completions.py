from fastapi import APIRouter

from api.v1.endpoints.gpt.schemas import CreateCompletionRequestDTO
from openai.types.chat.chat_completion import ChatCompletion

from core.config import config

chat_completions_router = APIRouter()

@chat_completions_router.post('/chat/completions', response_model=ChatCompletion)
async def create_chat_completions(dto: CreateCompletionRequestDTO):
    messages = [{'role': message.role, 'content': message.content} for message in dto.messages]

    request = await config.async_openai_client.chat.completions.create(
        model=dto.model,
        messages=messages,
        max_tokens=dto.max_tokens,
        temperature=dto.temperature
    )

    return request