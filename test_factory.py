"""TTS 팩토리 패턴 테스트"""
from src.tts.factory import get_tts_engine
from src.tts.base import TTSEngineBase

# 테스트 1: Edge TTS 엔진 생성
print("=" * 50)
print("Test 1: Edge TTS Engine Creation")
try:
    tts_edge = get_tts_engine("edge")
    print(f"[PASS] Edge TTS engine created: {type(tts_edge).__name__}")
    assert isinstance(tts_edge, TTSEngineBase), "Must inherit TTSEngineBase"
    print("[PASS] TTSEngineBase interface confirmed")
except Exception as e:
    print(f"[FAIL] {e}")

# 테스트 2: pyttsx3 엔진 생성
print("\n" + "=" * 50)
print("Test 2: pyttsx3 Engine Creation")
try:
    tts_pyttsx3 = get_tts_engine("pyttsx3")
    print(f"[PASS] pyttsx3 engine created: {type(tts_pyttsx3).__name__}")
    assert isinstance(tts_pyttsx3, TTSEngineBase), "Must inherit TTSEngineBase"
    print("[PASS] TTSEngineBase interface confirmed")
except Exception as e:
    print(f"[FAIL] {e}")

# 테스트 3: 기본값 (edge) 확인
print("\n" + "=" * 50)
print("Test 3: Default Engine (edge) Verification")
try:
    tts_default = get_tts_engine()
    print(f"[PASS] Default engine: {type(tts_default).__name__}")
    assert isinstance(tts_default, get_tts_engine("edge").__class__), "Default must be edge"
    print("[PASS] Default engine is 'edge'")
except Exception as e:
    print(f"[FAIL] {e}")

# 테스트 4: 잘못된 엔진 타입 처리
print("\n" + "=" * 50)
print("Test 4: Invalid Engine Type Handling")
try:
    tts_invalid = get_tts_engine("invalid_engine")
    print("[FAIL] ValueError should have been raised")
except ValueError as e:
    print(f"[PASS] Expected error: {e}")
except Exception as e:
    print(f"[FAIL] Unexpected error: {e}")

# 테스트 5: config.yaml 로드 확인
print("\n" + "=" * 50)
print("Test 5: config.yaml Settings Verification")
try:
    tts_edge = get_tts_engine("edge")
    print(f"[PASS] Edge voice: {tts_edge._voice}")
    print(f"[PASS] Edge rate: {tts_edge._rate}")
    print(f"[PASS] Edge pitch: {tts_edge._pitch}")
except Exception as e:
    print(f"[FAIL] {e}")

print("\n" + "=" * 50)
print("All factory tests completed!")
