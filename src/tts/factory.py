"""TTS 엔진 팩토리 - 엔진 유형에 따라 적절한 TTS 엔진 반환"""
import yaml
from pathlib import Path
from .base import TTSEngineBase
from .pyttsx3_engine import Pyttsx3Engine
from .edge_engine import EdgeEngine


def get_tts_engine(engine_type: str = "edge", config: dict = None) -> TTSEngineBase:
    """
    TTS 엔진 팩토리 함수

    Args:
        engine_type: 엔진 유형 ("edge" 또는 "pyttsx3")
        config: 엔진 설정 dict (기본값: config.yaml에서 읽음)

    Returns:
        TTSEngineBase의 구현체 (EdgeEngine 또는 Pyttsx3Engine)

    Raises:
        ValueError: 지원하지 않는 엔진 타입인 경우
        FileNotFoundError: config.yaml을 찾을 수 없는 경우
    """
    # config가 없으면 config.yaml에서 읽기
    if config is None:
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"config.yaml을 찾을 수 없습니다: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    engine_type = engine_type.lower().strip()

    if engine_type == "edge":
        return EdgeEngine(config)
    elif engine_type == "pyttsx3":
        return Pyttsx3Engine(config)
    else:
        raise ValueError(
            f"지원하지 않는 엔진 타입: {engine_type}. "
            f"지원 가능: 'edge', 'pyttsx3'"
        )
