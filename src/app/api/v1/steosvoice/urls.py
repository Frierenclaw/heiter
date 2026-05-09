from enum import Enum


class SteosVoiceURL(Enum):
    SYNTETHIS_BY_TEXT = 'https://public.api.voice.steos.io/api/v1/steos-voice-controller/available-voices/{steos_token}'
    