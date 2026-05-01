import whisper
import numpy as np

model = whisper.load_model("base")

def transcribe(audio_np: np.ndarray, sr: int = 16000) -> str:
    # Convert numpy array to float32 and resample if needed
    audio = whisper.pad_or_trim(audio_np.astype(np.float32))
    mel = whisper.log_mel_spectrogram(audio)
    result = whisper.decode(model, mel)
    return result.text