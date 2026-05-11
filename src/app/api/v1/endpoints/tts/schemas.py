from typing import Literal

from pydantic import BaseModel


class TTSApiSpeechRequestDTO(BaseModel):
    input: str
    model: Literal['steosvoice', 'frieren', 'edge_tts']
    voice: str

    speed: int = 1