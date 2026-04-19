"""
마이크 테스트 스크립트
- 사용 가능한 오디오 장치 목록 출력
- 스페이스바를 누르는 동안 녹음
- 녹음된 오디오 파형 정보 및 RMS 레벨 출력
- 녹음 파일을 test_recording.wav 로 저장
"""

import sys
import os

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import numpy as np
import sounddevice as sd
import wave
import keyboard
import time


def list_devices():
    print("=" * 60)
    print("사용 가능한 오디오 입력 장치 목록")
    print("=" * 60)
    devices = sd.query_devices()
    default_input = sd.default.device[0]
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            marker = " ◀ 기본값" if i == default_input else ""
            print(f"  [{i}] {dev['name']}{marker}")
            print(f"       채널: {dev['max_input_channels']}, 샘플레이트: {int(dev['default_samplerate'])}Hz")
    print()


def record_until_release(device=None, sample_rate=16000):
    chunks = []
    block_size = 1024

    def callback(indata, frames, time_info, status):
        if status:
            print(f"  [경고] {status}")
        chunks.append(indata.copy())

    print("  스페이스바를 누르고 말해주세요... (떼면 종료)")
    keyboard.wait("space")
    print("  🎤 녹음 중... (스페이스바를 떼면 종료)")

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        blocksize=block_size,
        device=device,
        callback=callback,
    ):
        start = time.time()
        time.sleep(block_size / sample_rate)  # 최소 1블록 캡처
        while keyboard.is_pressed("space"):
            elapsed = time.time() - start
            print(f"\r  녹음 중... {elapsed:.1f}초", end="", flush=True)
            if elapsed >= 30:
                print("\n  [경고] 30초 초과, 자동 종료")
                break
            time.sleep(0.05)

    print()
    if not chunks:
        return None
    return np.concatenate(chunks, axis=0)


def analyze(audio: np.ndarray, sample_rate: int):
    duration = len(audio) / sample_rate
    rms = float(np.sqrt(np.mean(audio ** 2)))
    peak = float(np.max(np.abs(audio)))
    silent = rms < 0.01

    print("=" * 60)
    print("녹음 분석 결과")
    print("=" * 60)
    print(f"  길이      : {duration:.2f}초 ({len(audio)} 샘플)")
    print(f"  RMS 레벨  : {rms:.5f}  (0.01 미만이면 무음 판정)")
    print(f"  최대 피크 : {peak:.5f}")
    print(f"  무음 판정 : {'⚠️  무음 (목소리가 녹음되지 않음)' if silent else '✅ 음성 감지됨'}")
    print()


def save_wav(audio: np.ndarray, sample_rate: int, path: str = "test_recording.wav"):
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.flatten().tobytes())
    print(f"  💾 저장됨: {path}")
    print(f"     (미디어 플레이어로 열어서 소리가 녹음됐는지 확인하세요)")
    print()


def main():
    sample_rate = 16000
    device = None  # None = 기본 마이크

    # 커맨드라인 인자로 장치 번호 지정 가능
    # 예: python test_mic.py 2
    if len(sys.argv) > 1:
        try:
            device = int(sys.argv[1])
            print(f"[설정] 장치 번호 {device} 사용\n")
        except ValueError:
            print(f"[오류] 장치 번호는 숫자여야 합니다: {sys.argv[1]}\n")

    list_devices()

    while True:
        print("=" * 60)
        print("마이크 테스트")
        print("  q 입력 후 Enter → 종료")
        print("  다른 장치 번호 입력 후 Enter → 해당 장치로 변경")
        print("  Enter만 입력 → 기본 마이크로 녹음 시작")
        print("=" * 60)
        cmd = input(f"장치 번호 (현재: {'기본값' if device is None else device}) > ").strip()

        if cmd.lower() == "q":
            print("종료합니다.")
            break
        elif cmd == "":
            pass
        elif cmd.isdigit():
            device = int(cmd)
            print(f"장치 {device} 로 변경됨\n")
            continue

        try:
            audio = record_until_release(device=device, sample_rate=sample_rate)
            if audio is None:
                print("  [오류] 녹음된 데이터 없음\n")
                continue
            analyze(audio, sample_rate)
            save_wav(audio, sample_rate)
        except Exception as e:
            print(f"\n  [오류] {e}")
            print("  → 장치 번호를 변경해서 다시 시도하세요\n")


if __name__ == "__main__":
    main()
