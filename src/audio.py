import time as time_module

import numpy as np
import sounddevice as sd


class AudioRecorder:
    def __init__(self, config: dict):
        self._sample_rate = config.get("sample_rate", 16000)
        self._device = config.get("audio_device", None)

    def record_until_release(self, ptt_handler, max_duration: int = 30) -> np.ndarray:
        chunks = []
        sample_rate = self._sample_rate
        block_size = 1024

        def callback(indata, frames, time, status):
            chunks.append(indata.copy())

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            blocksize=block_size,
            device=self._device,
            callback=callback,
        ):
            start = time_module.time()
            # 최소 1블록(약 23ms) 캡처 후 키 상태 확인 — 빠른 탭 race condition 완화
            time_module.sleep(block_size / sample_rate)
            while ptt_handler.is_pressed():
                if time_module.time() - start >= max_duration:
                    break
                time_module.sleep(0.01)

        if not chunks:
            return np.zeros((0, 1), dtype="float32")
        return np.concatenate(chunks, axis=0)

    def is_silent(self, audio: np.ndarray, threshold: float = 0.01) -> bool:
        if audio.size == 0:
            return True
        rms = float(np.sqrt(np.mean(audio ** 2)))
        return rms < threshold
