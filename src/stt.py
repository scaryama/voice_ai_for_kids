from typing import Optional
import numpy as np
import torch
import whisper

class STTEngine:
    def __init__(self, config: dict):
        """STT 엔진 초기화 (GPU 자동 감지)"""
        self._model = whisper.load_model("small")
        # Mac silicon은 mps, 일반 CUDA는 cuda, 나머지는 cpu
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        try:
            self._model = self._model.to(device)
        except (NotImplementedError, RuntimeError):
            # MPS 호환성 문제 시 CPU로 폴백
            print(f"[STT] {device} 호환성 문제, CPU로 변경")
            device = "cpu"
            self._model = self._model.to(device)

        print(f"[STT] Whisper device: {self._model.device}")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """
        음성을 텍스트로 변환 (GPU 가속)
        """
        if audio.size == 0:
            return None

        # 음성 전처리
        audio_mono = audio.flatten().astype(np.float32)

        # 저수준 API 사용 (GPU 명시적 활용)
        audio_padded = whisper.pad_or_trim(audio_mono)
        mel = whisper.log_mel_spectrogram(audio_padded).to(self._model.device)

        use_fp16 = self._model.device.type in ("cuda", "mps")
        options = whisper.DecodingOptions(language="ko", fp16=use_fp16)
        result = whisper.decode(self._model, mel, options)
        text = result.text.strip()

        return text if text else None
