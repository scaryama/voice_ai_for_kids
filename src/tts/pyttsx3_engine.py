"""pyttsx3 기반 TTS 엔진"""
import pyttsx3
from .base import TTSEngineBase


class Pyttsx3Engine(TTSEngineBase):
    """pyttsx3를 사용하는 TTS 엔진 (Windows/Mac/Linux)"""

    def __init__(self, config: dict = None):
        """
        pyttsx3 TTS 엔진 초기화

        Args:
            config: 설정 dict (rate, voice 등, 선택사항)
        """
        self._rate = (config or {}).get("tts_rate")
        self._voice_id = (config or {}).get("tts_voice")

    def speak(self, text: str) -> None:
        """텍스트를 음성으로 출력"""
        engine = pyttsx3.init()

        # 음성 설정
        if self._voice_id:
            engine.setProperty("voice", self._voice_id)

        # 속도 설정
        if self._rate is not None:
            engine.setProperty("rate", self._rate)

        # 재생
        engine.say(text)
        engine.runAndWait()
        engine.stop()
