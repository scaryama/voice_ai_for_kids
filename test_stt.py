"""STT 최소 테스트 — 스페이스바 녹음 후 Whisper 변환"""
import sys, time
import numpy as np
import sounddevice as sd
import keyboard
import whisper

SR = 16000

print("Whisper medium 모델 로딩 중... (처음엔 수십 초 걸릴 수 있음)")
t0 = time.time()
model = whisper.load_model("medium")
print(f"모델 로드 완료 ({time.time()-t0:.1f}초)\n")

print("스페이스바를 누르고 말하세요 (떼면 인식 시작)")
keyboard.wait("space")
print("🎤 녹음 중...")

chunks = []
with sd.InputStream(samplerate=SR, channels=1, dtype="float32",
                    callback=lambda d,f,t,s: chunks.append(d.copy())):
    time.sleep(0.05)
    while keyboard.is_pressed("space"):
        time.sleep(0.01)

audio = np.concatenate(chunks).flatten() if chunks else np.zeros(SR, dtype="float32")
print(f"녹음 완료 ({len(audio)/SR:.1f}초, RMS={np.sqrt(np.mean(audio**2)):.4f})\n")

print("⏳ 음성 인식 중...")
t0 = time.time()
result = model.transcribe(audio, language="ko", fp16=False)
print(f"완료 ({time.time()-t0:.1f}초)")
print(f"\n인식 결과: {result['text'].strip()}")
