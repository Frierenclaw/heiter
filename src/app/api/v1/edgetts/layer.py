import io

import edge_tts


class EdgeTTS:
    @staticmethod
    async def synthesis_by_text(
        input_text: str,
        voice: str
    ):
        communicate  = edge_tts.Communicate(
            text=input_text,
            voice=voice
        )

        return communicate