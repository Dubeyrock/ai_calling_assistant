import os
from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
REDIS_URL = os.getenv("REDIS_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL")
MONGO_URL = os.getenv("MONGO_URL")
