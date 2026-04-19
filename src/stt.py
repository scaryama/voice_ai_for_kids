from typing import Optional
import numpy as np
import whisper


class STTEngine:
    def __init__(self, config: dict):
        self._model = whisper.load_model("medium")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        if audio.size == 0:
            return None
        audio_mono = audio.flatten().astype(np.float32)
        result = self._model.transcribe(audio_mono, language="ko", fp16=False)
        text = result.get("text", "").strip()
        return text if text else None
