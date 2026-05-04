from pydantic import BaseModel


class MessageDTO(BaseModel):
    role: str
    content: str

class CreateCompletionRequestDTO(BaseModel):
    model: str = 'codestral-latest'
    messages: list[MessageDTO]

    max_tokens: int | None = None
    temperature: float = 1.0
    
    use_previous_context: bool = True