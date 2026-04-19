from pathlib import Path
from datetime import datetime
import numpy as np
import soundfile as sf


class AudioLogger:
    """사용자 음성을 WAV와 텍스트로 logs 폴더에 저장"""

    def __init__(self, logs_dir: str = "logs"):
        self._logs_dir = Path(logs_dir)
        self._logs_dir.mkdir(exist_ok=True)
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._turn = 0

    def save_user_audio(self, audio: np.ndarray, text: str, sample_rate: int = 16000) -> None:
        """
        사용자 음성과 텍스트를 저장

        Args:
            audio: 음성 데이터 (numpy array)
            text: STT 결과 텍스트
            sample_rate: 샘플링 레이트 (기본값: 16000)
        """
        self._turn += 1
        filename_base = self._logs_dir / f"{self._session_id}_{self._turn:03d}"

        # WAV 파일 저장
        wav_file = f"{filename_base}.wav"
        sf.write(wav_file, audio, sample_rate)

        # 텍스트 파일 저장 (순수 텍스트만)
        txt_file = f"{filename_base}.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(text)
