import io
import av
import edge_tts

class EdgeTTSStreamer:
    def __init__(self, text: str, voice: str):
        self.text = text
        self.voice = voice

    async def stream(self):
        communicate = edge_tts.Communicate(text=self.text, voice=self.voice)
        
        mp3_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_buffer.write(chunk["data"])
        
        mp3_buffer.seek(0)
        
        container = av.open(mp3_buffer)
        audio_stream = container.streams.audio[0]
        
        resampler = av.AudioResampler(
            format='s16',     # 16-bit
            layout='mono',    # Mono
            rate=16000        # 16 kHz 
        )
        
        for frame in container.decode(audio_stream):
            resampled_frames = resampler.resample(frame)
            for r_frame in resampled_frames:
                audio_data = r_frame.to_ndarray().tobytes()
                
                yield {"type": "audio", "data": audio_data}


class EdgeTTS:
    @staticmethod
    async def synthesis_by_text(
        input_text: str,
        voice: str
    ):
        return EdgeTTSStreamer(text=input_text, voice=voice)