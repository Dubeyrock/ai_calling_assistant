import sounddevice as sd
import numpy as np
from core.stt import transcribe
from core.llm import get_llm_response
from core.tts import speak

def record_audio(duration=5, samplerate=16000):
    print("🎤 Listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
    sd.wait()
    return audio.flatten(), samplerate

def main():
    session_id = "cli_user"
    print("AI Calling Assistant (say 'exit' to quit)")
    while True:
        audio, sr = record_audio()
        text = transcribe(audio, sr)
        print(f"You: {text}")
        if "exit" in text.lower():
            break
        reply = get_llm_response(text, session_id, source="cli")
        print(f"AI: {reply}")
        speak(reply)

if __name__ == "__main__":
    main()