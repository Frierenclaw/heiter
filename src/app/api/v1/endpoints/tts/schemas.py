from typing import Literal

from pydantic import BaseModel


class TTSApiSpeechRequestDTO(BaseModel):
    input: str
    model: Literal['steosvoice', 'frieren']
    voice: str

    speed: int = 1