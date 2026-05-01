import redis
import json
from config import REDIS_URL

# Lazy Redis connection
r = None

def _connect_redis():
    global r
    if r is None and REDIS_URL:
        try:
            r = redis.from_url(REDIS_URL)
            r.ping()  # Test connection
            print("✓ Redis connected")
        except Exception as e:
            print(f"⚠ Redis not available: {str(e)[:50]}... (continuing without cache)")
            r = None
    return r

def get_history(session_id: str, max_len=10):
    try:
        redis_conn = _connect_redis()
        if redis_conn:
            data = redis_conn.lrange(f"chat:{session_id}", -max_len, -1)
            return [json.loads(x) for x in data]
    except Exception as e:
        print(f"⚠ Could not retrieve history: {str(e)[:50]}")
    return []

def add_to_history(session_id: str, user_msg: str, bot_msg: str):
    try:
        redis_conn = _connect_redis()
        if redis_conn:
            entry = [{"role": "user", "content": user_msg},
                     {"role": "assistant", "content": bot_msg}]
            redis_conn.rpush(f"chat:{session_id}", json.dumps(entry[0]), json.dumps(entry[1]))
            redis_conn.expire(f"chat:{session_id}", 3600)
    except Exception as e:
        print(f"⚠ Could not save history: {str(e)[:50]}")