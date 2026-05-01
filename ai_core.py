import os
import wave
import pyaudio
import numpy as np
from dotenv import load_dotenv
import openai
from groq import Groq
from elevenlabs.client import ElevenLabs
import tempfile
import pygame
import io

load_dotenv()

# ElevenLabs
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY_"))

# Whisper (local faster-whisper or OpenAI API)
# Option A: Use OpenAI Whisper API (simpler)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Conversation memory
conversation_history = []   # list of {"role": "user"/"assistant", "content": str}

def record_audio(duration=5, sample_rate=16000):
    """Record from microphone for `duration` seconds -> returns audio bytes"""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)
    frames = []
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return b''.join(frames)

def save_audio_bytes_to_wav(audio_bytes, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(16000)
        wf.writeframes(audio_bytes)

def transcribe_audio(audio_bytes):
    """STT using OpenAI Whisper API (or local)"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        save_audio_bytes_to_wav(audio_bytes, tmp.name)
        tmp_path = tmp.name
    with open(tmp_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.unlink(tmp_path)
    return transcript["text"]

def get_llm_response(user_text):
    """Call Groq LLM with conversation memory"""
    conversation_history.append({"role": "user", "content": user_text})
    # System prompt for HR / job assistant (customize)
    system_prompt = "You are an AI calling assistant for a recruitment system. Answer concisely and helpfully."
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

def text_to_speech_and_play(text):
    """TTS via ElevenLabs and play through speakers"""
    try:
        audio = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        )
        pygame.mixer.init()
        sound = pygame.mixer.Sound(io.BytesIO(audio))
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
    except Exception as e:
        print(f"TTS Error: {e}")

# Optional: Use local Whisper (free, no API key)
# pip install faster-whisper
# from faster_whisper import WhisperModel
# model = WhisperModel("base", device="cpu", compute_type="int8")
# def transcribe_local(audio_bytes): ...