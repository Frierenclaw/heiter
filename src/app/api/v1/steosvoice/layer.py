import base64
import json

from api.v1.steosvoice.urls import SteosVoiceURL
from core.clients import steos_voice_client


class SteosVoice:
    @staticmethod
    async def synthesis_by_text(input_text: str,
                                speed: int,
                                steos_token: str) -> bytes:
        """
        Synthesizes speech from the given text using the Steos Voice API.

        Args:
            input_text (str): The text to be synthesized into speech.
            speed (int): The speed multiplier for the speech synthesis.
            steos_token (str): The authentication token for the Steos Voice API.

        Returns:
            bytes: The synthesized audio data as bytes.
        """

        payload = {'voiceId': 1,
                   'text': input_text,
                   'speedMultiplier': speed}
        
        request = await steos_voice_client.post(
            url=SteosVoiceURL.value.format(steos_token=steos_token),
            json=payload
        )

        request_serialized = json.loads(request.text)
        file_contents = request_serialized.get('fileContents')

        return base64.b64decode(file_contents)
    