import asyncio
import base64
import json
import logging
from io import BytesIO
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import whisper
import numpy as np
import wave

from core.llm import get_llm_response_stream
from core.tts import stream_audio
from config import WHISPER_MODEL

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FreeSWITCH-Server")

app = FastAPI()

# Load local whisper tiny model in memory for super-fast transcription
# You can switch to OpenAI Whisper API if local computation is heavy
logger.info(f"Loading Whisper model: {WHISPER_MODEL}...")
stt_model = whisper.load_model("tiny")
logger.info("Whisper model loaded!")

@app.websocket("/fs-media")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket Server for FreeSWITCH mod_audio_fork / SIP Streaming
    FreeSWITCH streams audio here, we transcribe -> llm -> tts -> stream back.
    """
    await websocket.accept()
    logger.info("WebSocket connection established with FreeSWITCH.")
    session_id = "call_" + str(id(websocket))
    
    try:
        audio_buffer = bytearray()
        
        while True:
            # 1. Receive JSON payload with Base64 audio from FreeSWITCH
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data['event'] == "media":
                # Decode audio bytes (L16 payload)
                payload = base64.b64decode(data['media']['payload'])
                audio_buffer.extend(payload)
                
                # Check if we have enough buffer (e.g., 2 seconds of silence/speech)
                # For a production system, we'd use Voice Activity Detection (VAD) here
                if len(audio_buffer) >= 32000 * 2: # ~2 seconds of 16k mono audio
                    logger.info("Processing audio chunk...")
                    
                    # Convert bytearray to valid Numpy Array for Whisper
                    audio_np = np.frombuffer(audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # 2. Transcribe immediately
                    result = stt_model.transcribe(audio_np, fp16=False)
                    user_text = result["text"].strip()
                    logger.info(f"User Transcribed: {user_text}")
                    
                    audio_buffer.clear() # Reset buffer
                    
                    if user_text:
                        # 3. Stream Groq LLM Response
                        text_iterator = get_llm_response_stream(user_text, session_id=session_id)
                        
                        # 4. Stream Audio back to FreeSWITCH via ElevenLabs using the generator
                        for audio_chunk in stream_audio(text_iterator):
                            # Send back to FreeSWITCH via WEbSocket (Base64 encoded)
                            reply_payload = {
                                "event": "media",
                                "media": {
                                    "payload": base64.b64encode(audio_chunk).decode('utf-8')
                                }
                            }
                            await websocket.send_text(json.dumps(reply_payload))
                            # Add tiny sleep to prevent flooding socket
                            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        logger.info(f"FreeSWITCH disconnected. Session: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")

if __name__ == "__main__":
    uvicorn.run("fs_server:app", host="0.0.0.0", port=8000, reload=True)
