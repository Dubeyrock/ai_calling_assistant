from elevenlabs.client import ElevenLabs
import pygame
import io
from config import ELEVENLABS_API_KEY

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak(text: str):
    """Generate and play speech using ElevenLabs API"""
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        )
        
        # Play audio using pygame
        pygame.mixer.init()
        sound = pygame.mixer.Sound(io.BytesIO(audio))
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
    except Exception as e:
        print(f"⚠ TTS Error: {str(e)[:100]} (continuing without audio)")

def stream_audio(text_iterator, voice_id="21m00Tcm4TlvDq8ikWAM"):
    """
    Streams audio bytes chunk-by-chunk from ElevenLabs using a text iterator.
    """
    try:
        # ElevenLabs library natively supports streaming from a text generator
        audio_stream = client.text_to_speech.convert_as_stream(
            text=text_iterator,
            voice_id=voice_id,
        )
        for chunk in audio_stream:
            yield chunk
    except Exception as e:
        print(f"⚠ Stream TTS Error: {e}")