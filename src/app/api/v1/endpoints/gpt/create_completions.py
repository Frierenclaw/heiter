from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from openai import APITimeoutError, OpenAIError, RateLimitError
from openai.types.chat.chat_completion import ChatCompletion

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.gpt.schemas import CreateCompletionRequestDTO
from core.config import async_openai_client
from models.user import User

chat_completions_router = APIRouter()


@chat_completions_router.post('/chat/completions', response_model=ChatCompletion)
async def create_chat_completions(dto: CreateCompletionRequestDTO,
                                  user: Annotated[User, Depends(get_current_user)]):
    messages = [{'role': message.role, 'content': message.content} for message in dto.messages]

    try:
        request = await async_openai_client.chat.completions.create(
            model=dto.model,
            messages=messages,
            max_tokens=dto.max_tokens,
            temperature=dto.temperature
        )
    except RateLimitError as e:
        logger.error(f'GPT Rate limit has exceeded . Detail error: {e}. Request by user {user.id}')
        
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,  # noqa: B904
                            detail='Global rate limit has exceeded') 
    except APITimeoutError as e:
        logger.error(f'GPT Timeout. Detail error: {e}')

        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,  # noqa: B904
                            detail='Internal request timeout. Try again later')
    except OpenAIError as e:
        logger.error(f'OpenAI Error. Detail error: {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
                            detail='Internal error. Try again later')
    except Exception as e:
        logger.error(f'Unexcepted error. Detail error: {e}')
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # noqa: B904
                            detail='Internal server error. Try again later')
    
    return request