from typing import Literal

from pydantic import BaseModel


class MessageDTO(BaseModel):
    role: Literal['user', 'system', 'assistant']
    content: str

class CreateCompletionRequestDTO(BaseModel):
    model: str = 'codestral-latest'
    messages: list[MessageDTO]

    max_tokens: int | None = None
    temperature: float = 1.0

    stream: bool = True