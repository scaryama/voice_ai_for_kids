import sys
import os

# Windows 터미널 UTF-8 출력 보장
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import torch
print(f"CUDA available: {torch.cuda.is_available()}")

import yaml
from dotenv import load_dotenv

load_dotenv()

from src.debug import DebugLogger
from src.memory import ConversationMemory
from src.ptt import PTTHandler
from src.audio import AudioRecorder
from src.audio_logger import AudioLogger
from src.stt import STTEngine
from src.llm import LLMClient
from src.tts import get_tts_engine


def load_config(path: str = "config.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    log = DebugLogger()
    memory = ConversationMemory()
    ptt = PTTHandler(config)
    recorder = AudioRecorder(config)
    audio_logger = AudioLogger()
    tts = get_tts_engine("edge", config)

    log.log_status("KidVoice AI 시작 — Whisper 모델 로딩 중...")
    stt = STTEngine(config)
    llm = LLMClient(config)
    log.log_status("모델 로드 완료")

    # AI가 먼저 말하기 — BOOTSTRAP 컨텍스트 기반 첫 인사
    log.log_status("💭 AI 첫 인사 생성 중...")
    history = memory.load()
    try:
        greeting = llm.chat("대화를 이어서 해줘.", history)
    except Exception:
        greeting = "안녕! 무엇이 궁금해?"
    log.log_conversation("AI", greeting)
    memory.append("ai", greeting)
    log.log_status("🔊 AI 첫 인사 출력...")
    tts.speak(greeting)

    while True:
        tts.speak("스페이스바 누르면서 말해줘")
        log.log_status("스페이스바를 기다리는 중...")
        ptt.wait_for_press()

        log.log_status("🎤 녹음 중...")
        audio = recorder.record_until_release(ptt, max_duration=config.get("max_duration", 30))

        if recorder.is_silent(audio):
            log.log_error("무음 감지")
            tts.speak_error()
            continue

        tts.speak("Okay")
        log.log_status("⏳ 음성 인식 중...")
        text = stt.transcribe(audio, sample_rate=config.get("sample_rate", 16000))

        if not text:
            log.log_error("STT 실패")
            tts.speak_error()
            continue

        log.log_conversation("아이", text)
        audio_logger.save_user_audio(audio, text, sample_rate=config.get("sample_rate", 16000))

        log.log_status("💭 AI 생각 중...")
        history = memory.load()
        memory.append("child", text)
        try:
            answer = llm.chat(text, history)
        except Exception as e:
            log.log_error(f"LLM 오류: {e}")
            tts.speak_error()
            continue

        if not answer:
            log.log_error("LLM 응답 없음")
            tts.speak_error()
            continue

        log.log_conversation("AI", answer)
        memory.append("ai", answer)

        log.log_status("🔊 음성 출력 중...")
        tts.speak(answer)


if __name__ == "__main__":
    main()
