import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.stt import transcribe
from core.llm import get_llm_response
from core.tts import speak
import wave
import numpy as np

AUDIO_DIR = r"C:\calls"
PROCESSED_DIR = r"C:\calls\processed"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

class CallHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".wav") and "incoming" in event.src_path:
            print(f"New call recording: {event.src_path}")
            time.sleep(1)  # wait for write to finish
            # Transcribe
            audio_np, samplerate = read_wav(event.src_path)
            user_text = transcribe(audio_np, samplerate)
            if user_text:
                reply = get_llm_response(user_text, session_id="sip_call")
                # Generate TTS and save as reply.wav
                from elevenlabs.client import ElevenLabs
                from config import ELEVENLABS_API_KEY
                elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                audio = elevenlabs_client.text_to_speech.convert(
                    text=reply,
                    voice_id="21m00Tcm4TlvDq8ikWAM"  # Rachel voice
                )
                reply_path = os.path.join(AUDIO_DIR, "reply.wav")
                with open(reply_path, "wb") as f:
                    f.write(audio)
                # Now we need to play this file back through PJSIP.
                # PJSIP CLI can play a file to the active call using --play-file.
                # We'll use subprocess to send command.
                import subprocess
                subprocess.run([r"C:\pjsip\bin\pjsua-x86_64.exe", "--play-file", reply_path])
            # Move processed file
            os.rename(event.src_path, os.path.join(PROCESSED_DIR, os.path.basename(event.src_path)))

def read_wav(path):
    with wave.open(path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        samplerate = wf.getframerate()
    return audio, samplerate

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CallHandler(), path=AUDIO_DIR, recursive=False)
    observer.start()
    print("SIP Bot watching for incoming calls...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()