import json
from datetime import datetime

def log_transcript(user_text, assistant_text, session_id=None):
    if session_id is None:
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "user": user_text,
        "assistant": assistant_text
    }
    with open(f"transcripts/{session_id}.json", "a") as f:
        json.dump(log_entry, f)
        f.write("\n")