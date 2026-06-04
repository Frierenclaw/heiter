import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from loguru import logger
from openai import APITimeoutError, OpenAIError, RateLimitError

from api.v1.dependencies.auth import get_current_user
from api.v1.endpoints.gpt.schemas import CreateCompletionRequestDTO
from core.clients import async_openai_client
from models.user import User
from redis_db import RedisClient

chat_completions_router = APIRouter()


@chat_completions_router.post('/chat/completions')
async def create_chat_completions(
    dto: CreateCompletionRequestDTO,
    user: Annotated[User, Depends(get_current_user)]
):
    """
    Create chat completions using OpenAI's API with streaming support.
    """
    
    new_messages = [{'role': message.role, 'content': message.content} for message in dto.messages]
    request_messages = []

    if dto.use_previous_context:
        context_messages = await RedisClient.get_context(
            user_id=user.id
        )
        request_messages.extend(context_messages)
        
    request_messages.extend(new_messages)

    async def generate_stream():
        full_assistant_message = ""
        
        try:
            stream = await async_openai_client.chat.completions.create(
                model=dto.model,
                messages=request_messages,
                max_tokens=dto.max_tokens,
                temperature=dto.temperature,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    full_assistant_message += chunk.choices[0].delta.content

                yield f"data: {chunk.model_dump_json()}\n\n"
            
            yield "data: [DONE]\n\n"

            if dto.use_previous_context and full_assistant_message:
                to_save = [
                    new_messages[-1], 
                    {'role': 'assistant', 'content': full_assistant_message}
                ]
                await RedisClient.put_in_context(
                    user_id=user.id,
                    messages=to_save
                )

        except Exception as e:
            logger.error(f'Streaming error for user {user.id}: {e}')

    try:
        if dto.stream:
            return StreamingResponse(generate_stream(), media_type="text/event-stream")

        response = await async_openai_client.chat.completions.create(
            model=dto.model,
            messages=request_messages,
            max_tokens=dto.max_tokens,
            temperature=dto.temperature,
            stream=False
        )

        if dto.use_previous_context:
            assistant_msg = response.choices[0].message
            to_save = [new_messages[-1], {'role': 'assistant', 'content': assistant_msg.content}]
            await RedisClient.put_in_context(
                user_id=user.id,
                messages=to_save
            )
            
        return response

    except RateLimitError as e:
        logger.error(f'GPT Rate limit has exceeded . Detail error: {e}. Request by user {user.id}')
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail='Global rate limit has exceeded')
    except APITimeoutError as e:
        logger.error(f'GPT Timeout. Detail error: {e}')
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail='Internal request timeout. Try again later')
    except OpenAIError as e:
        logger.error(f'OpenAI Error. Detail error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal error. Try again later')
    except Exception as e:
        logger.error(f'Unexpected error. Detail error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Internal server error. Try again later')