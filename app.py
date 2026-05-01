import streamlit as st
import tempfile
import whisper
import os
import socket
from core.stt import transcribe
from core.llm import get_llm_response
from core.tts import client as elevenlabs_client
from config import GROQ_API_KEY, ELEVENLABS_API_KEY

# Page Config
st.set_page_config(page_title="AI Calling Assistant", page_icon="📞", layout="wide")

# --- Helper Functions ---
def check_connection(host, port):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

# --- Sidebar: Dashboard & Status ---cd
st.sidebar.title("🛠 Admin Dashboard")

status_container = st.sidebar.container(border=True)
status_container.subheader("System Status")

# 1. FreeSWITCH Status (Default ESL port 8021)
fs_online = check_connection("localhost", 8021)
status_container.write(f"FreeSWITCH: {'🟢 Online' if fs_online else '🔴 Offline'}")

# 2. API Status
groq_ready = GROQ_API_KEY is not None and len(GROQ_API_KEY) > 10
eleven_ready = ELEVENLABS_API_KEY is not None and len(ELEVENLABS_API_KEY) > 10
status_container.write(f"Groq API: {'🟢 Ready' if groq_ready else '🔴 Missing Key'}")
status_container.write(f"ElevenLabs: {'🟢 Ready' if eleven_ready else '🔴 Missing Key'}")

# --- Sidebar: Settings ---
st.sidebar.title("⚙ Settings")

system_prompt = st.sidebar.text_area(
    "AI Personality (System Prompt)", 
    value="You are a helpful AI assistant for a business portal. Be professional but friendly.",
    height=150
)

voice_options = {
    "Rachel (Female)": "21m00Tcm4TlvDq8ikWAM",
    "Bella (Female)": "EXAVITQu4vr4xnNLMQic",
    "Antoni (Male)": "ErXw9S1kgoSYNrSclH2u",
    "Josh (Male)": "TxGEqnHW4m3z4H957vT2"
}
selected_voice_name = st.sidebar.selectbox("Choose AI Voice", list(voice_options.keys()))
selected_voice_id = voice_options[selected_voice_name]

if st.sidebar.button("🗑 Clear Chat History"):
    st.session_state.history = []
    st.rerun()

# --- Main App Interface ---
st.title("📞 AI  Calling System")
st.markdown("---")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display Chat History 
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio" in msg and msg["audio"] is not None:
                st.audio(msg["audio"], format="audio/mp3")

# Footer for Recording
st.markdown("### 🎤 Speak to the Assistant")
audio_value = st.audio_input("Record your message")

if audio_value is not None:
    # Process only if this is a new audio submission
    if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio_value:
        st.session_state.last_processed_audio = audio_value
        
        # 1. Save browser audio bytes to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_value.getvalue())
            tmp_file_path = tmp_file.name
            
        # 2. Transcribe using Whisper
        with st.spinner("Transcribing your voice..."):
            try:
                audio_np = whisper.load_audio(tmp_file_path)
                user_text = transcribe(audio_np)
            except Exception as e:
                st.error(f"Error processing audio: {e}")
                user_text = ""
            finally:
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                
        # 3. Process LLM & TTS
        if user_text.strip():
            # Show the user's message
            st.session_state.history.append({"role": "user", "content": user_text})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_text)
                
            # Get AI response with custom system prompt
            with st.spinner("AI is thinking..."):
                reply = get_llm_response(user_text, session_id="web_user", system_prompt=system_prompt)
            
            # Generate TTS Bytes using selected voice
            with st.spinner(f"Generating voice ({selected_voice_name})..."):
                try:
                    audio_bytes_raw = elevenlabs_client.text_to_speech.convert(
                        text=reply,
                        voice_id=selected_voice_id
                    )
                    # Handle generator if needed
                    audio_bytes = b"".join(list(audio_bytes_raw)) if not isinstance(audio_bytes_raw, bytes) else audio_bytes_raw
                except Exception as e:
                    st.warning(f"TTS Error: {e}")
                    audio_bytes = None
            
            # Show AI response and Audio
            st.session_state.history.append({"role": "assistant", "content": reply, "audio": audio_bytes})
            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            
            st.rerun() # Refresh to show message in chat flow properly
        else:
            st.warning("Could not hear you clearly. Please speak again.")

