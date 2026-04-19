"""TTS 엔진 추상 기본 클래스"""
from abc import ABC, abstractmethod

ERROR_MESSAGE = "다시 한번 말해줘"


class TTSEngineBase(ABC):
    """TTS 엔진 인터페이스"""

    @abstractmethod
    def speak(self, text: str) -> None:
        """텍스트를 음성으로 출력"""
        pass

    def speak_error(self) -> None:
        """에러 메시지 출력"""
        self.speak(ERROR_MESSAGE)
