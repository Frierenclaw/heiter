from typing import Annotated

from fastapi import APIRouter, Depends
from openai.types.chat.chat_completion import ChatCompletion

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.gpt.schemas import CreateCompletionRequestDTO
from core.config import config
from models.user import User

chat_completions_router = APIRouter()


@chat_completions_router.post('/chat/completions', response_model=ChatCompletion)
async def create_chat_completions(dto: CreateCompletionRequestDTO,
                                  user: Annotated[User, Depends(get_current_user)]):
    messages = [{'role': message.role, 'content': message.content} for message in dto.messages]

    request = await config.async_openai_client.chat.completions.create(
        model=dto.model,
        messages=messages,
        max_tokens=dto.max_tokens,
        temperature=dto.temperature
    )

    return request # codestral-latest