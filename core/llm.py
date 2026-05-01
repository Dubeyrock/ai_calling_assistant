from groq import Groq
from config import GROQ_API_KEY
from core.session import get_history, add_to_history
from storage.db import log_conversation   # import from storage/db.py

client = Groq(api_key=GROQ_API_KEY)

def get_llm_response(user_text: str, session_id: str, source: str = "web", system_prompt: str = None) -> str:
    # Retrieve conversation history
    history = get_history(session_id)
    
    # Use custom system prompt if provided, else default
    default_sys = "You are a helpful voice assistant for a job portal."
    messages = [
        {"role": "system", "content": system_prompt if system_prompt else default_sys},
        *history,
        {"role": "user", "content": user_text}
    ]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    
    # Save to memory (Redis) - safe to fail
    try:
        add_to_history(session_id, user_text, reply)
    except Exception as e:
        print(f"⚠ Could not save to history: {str(e)[:50]}")
    
    # Log to PostgreSQL + MongoDB - safe to fail
    try:
        log_conversation(session_id, user_text, reply, source)
    except Exception as e:
        print(f"⚠ Could not log conversation: {str(e)[:50]}")
    
    return reply

def get_llm_response_stream(user_text: str, session_id: str, system_prompt: str = None):
    # Retrieve conversation history
    history = get_history(session_id)
    default_sys = "You are a helpful voice assistant. Keep answers brief and conversational."
    messages = [
        {"role": "system", "content": system_prompt if system_prompt else default_sys},
        *history,
        {"role": "user", "content": user_text}
    ]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        stream=True
    )
    
    full_reply = ""
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            full_reply += delta
            yield delta
            
    # Save after stream finishes
    try:
        add_to_history(session_id, user_text, full_reply)
        log_conversation(session_id, user_text, full_reply, "stream")
    except Exception:
        pass