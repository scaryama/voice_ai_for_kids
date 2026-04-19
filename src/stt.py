from typing import Optional
import numpy as np
import whisper


class STTEngine:
    def __init__(self, config: dict):
        """STT 엔진 초기화 (GPU 자동 감지)"""
        self._model = whisper.load_model("small")
        # GPU 있으면 사용, 없으면 CPU (자동)
        print(f"[STT] Whisper device: {self._model.device}")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """
        음성을 텍스트로 변환

        주의: decode() 저수준 API는 한국어 처리 시 오버헤드가 있어
        고수준 API (transcribe)가 더 효율적입니다.
        GPU 추가 시 자동으로 활용됩니다.
        """
        if audio.size == 0:
            return None

        # 음성 전처리
        audio_mono = audio.flatten().astype(np.float32)

        # 고수준 API 사용 (한국어 최적화)
        result = self._model.transcribe(audio_mono, language="ko", fp16=False)
        text = result.get("text", "").strip()

        return text if text else None
