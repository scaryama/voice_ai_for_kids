"""TTS 최소 테스트 — 음성 출력 작동 확인 (아이 목소리)"""
import sys
import yaml
from dotenv import load_dotenv

# Windows 터미널 UTF-8 출력 보장
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

from src.tts import get_tts_engine
from src.tts.base import ERROR_MESSAGE

# 설정 로드
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print("TTS 엔진 초기화 중...")
# 테스트할 엔진 선택 (아래 중 하나 활성화)
#tts = get_tts_engine("pyttsx3", config)
tts = get_tts_engine("edge", config)
print(f"[OK] TTS 초기화 완료")
print(f"   Voice ID: {config.get('tts_voice', '기본값')}")
print(f"   Pitch (음역대): {config.get('tts_pitch', 1.6)}")
print(f"   Rate (속도): {config.get('tts_rate', 170)}\n")

# 테스트 1: 기본 음성 출력
print("=" * 60)
print("테스트 1: 기본 음성 출력 (안녕하세요!)")
print("=" * 60)
tts.speak("안녕하세요!")
print("[OK] 완료\n")

print("=" * 60)
print("[SUCCESS] TTS 아이 목소리 테스트 완료")
print("=" * 60)
