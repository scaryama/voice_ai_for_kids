"""STT 음성-텍스트 변환 시간 측정"""
import sys
import time
import numpy as np
from scipy.io import wavfile
from pathlib import Path

# Windows 터미널 UTF-8 출력
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.stt import STTEngine

# 설정
TEST_AUDIO_FILE = "test_recording.wav"
config = {}

print("=" * 70)
print("STT (Speech-to-Text) 시간 측정")
print("=" * 70)

# 1. 테스트 음성 파일 로드
print(f"\n[1] 테스트 음성 파일 로드: {TEST_AUDIO_FILE}")
audio_file = Path(TEST_AUDIO_FILE)
if not audio_file.exists():
    print(f"[ERROR] 파일을 찾을 수 없습니다: {TEST_AUDIO_FILE}")
    sys.exit(1)

sample_rate, audio_data = wavfile.read(TEST_AUDIO_FILE)
print(f"    Sample Rate: {sample_rate} Hz")
print(f"    Audio Duration: {len(audio_data) / sample_rate:.2f} seconds")
print(f"    Audio Shape: {audio_data.shape}")
print("[OK] 음성 파일 로드 완료\n")

# 2. STT 엔진 초기화
print("[2] STT 엔진 초기화 (Whisper 모델 로드 중...)")
start_init = time.time()
stt = STTEngine(config)
init_time = time.time() - start_init
print(f"[OK] 엔진 초기화 완료 ({init_time:.2f}초)\n")

# 3. 음성-텍스트 변환 (시간 측정)
print("[3] 음성-텍스트 변환 중...")
print("-" * 70)
start_transcribe = time.time()
text = stt.transcribe(audio_data, sample_rate=sample_rate)
transcribe_time = time.time() - start_transcribe
print("-" * 70)

# 4. 결과 출력
print(f"\n[OK] 변환 완료\n")

print("=" * 70)
print("결과 (Results)")
print("=" * 70)
print(f"변환된 텍스트: {text}")
print()
print("=" * 70)
print("시간 측정 (Timing)")
print("=" * 70)
print(f"엔진 초기화 시간: {init_time:.2f}초")
print(f"음성-텍스트 변환 시간: {transcribe_time:.2f}초")
print(f"총 시간: {init_time + transcribe_time:.2f}초")
audio_duration = len(audio_data) / sample_rate
print(f"\n음성 길이: {audio_duration:.2f}초")
print(f"변환 속도: {audio_duration / transcribe_time:.2f}x (실시간 기준)")
print("=" * 70)
