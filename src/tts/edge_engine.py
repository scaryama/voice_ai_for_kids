"""Edge TTS 기반 TTS 엔진"""
import asyncio
import tempfile
from pathlib import Path
import pygame

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

from .base import TTSEngineBase


class EdgeEngine(TTSEngineBase):
    """Edge TTS를 사용하는 TTS 엔진 (Windows/Mac 크로스플랫폼)"""

    def __init__(self, config: dict = None):
        """
        Edge TTS 엔진 초기화

        Args:
            config: 설정 dict (tts_voice, tts_rate, tts_pitch 등)
        """
        if not EDGE_TTS_AVAILABLE:
            raise ImportError(
                "edge-tts is not installed. Run: pip install edge-tts pygame"
            )

        config = config or {}
        self._voice = config.get("tts_voice", "ko-KR-SunHiNeural")
        self._rate = config.get("tts_rate")
        self._pitch = config.get("tts_pitch")
        self._temp_dir = tempfile.gettempdir()
        self._pygame_initialized = False

        self._init_pygame()

    def _init_pygame(self):
        """pygame 믹서 초기화"""
        try:
            pygame.mixer.init()
            self._pygame_initialized = True
        except Exception as e:
            print(f"[Warning] pygame mixer 초기화 실패: {e}")
            self._pygame_initialized = False

    def _speak_async(self, text: str) -> None:
        """Edge TTS 비동기 실행"""
        async def _async_tts():
            try:
                # 임시 파일 생성
                temp_file = Path(self._temp_dir) / f"tts_{id(text)}.mp3"

                # Edge TTS로 MP3 생성
                tts_kwargs = {
                    "text": text,
                    "voice": self._voice,
                }
                if self._rate is not None:
                    tts_kwargs["rate"] = self._rate
                if self._pitch is not None:
                    tts_kwargs["pitch"] = self._pitch

                communicate = edge_tts.Communicate(**tts_kwargs)
                await communicate.save(str(temp_file))

                # pygame로 재생
                if self._pygame_initialized:
                    pygame.mixer.music.load(str(temp_file))
                    pygame.mixer.music.play()
                    # 재생 완료까지 대기
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)

                # 임시 파일 정리
                try:
                    temp_file.unlink()
                except Exception:
                    pass

            except Exception as e:
                print(f"[Error] TTS 실행 실패: {e}")

        # 이벤트 루프 실행
        try:
            asyncio.run(_async_tts())
        except RuntimeError:
            # 이미 루프가 실행 중인 경우
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_async_tts())

    def speak(self, text: str) -> None:
        """텍스트를 음성으로 출력"""
        self._speak_async(text)
