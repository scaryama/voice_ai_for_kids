# 🎙️ KidVoice AI - 어린이 음성 대화 AI

> 어린이를 위한 음성 기반 AI 어시스턴트
> 자신의 정체성을 발견하면서 성장하는 AI와의 상호작용

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 개요

**KidVoice AI**는 어린이와 음성으로 대화하는 AI 어시스턴트입니다. 단순한 질답을 넘어, AI가 어린이와 함께 자신의 정체성을 발견해가는 **상호작용형 성장 경험**을 제공합니다.

### 🎯 특징

- **음성 기반 상호작용**: 스페이스바를 누르며 말하면 AI가 들어주고 답변합니다
- **어린이 맞춤형 음성**: Edge TTS로 5-7살 아이 톤의 한국어 음성 생성
- **AI 성장 시스템**: 부트스트랩 컨텍스트를 통해 AI가 어린이와 함께 정체성 구축
- **대화 메모리**: 전체 대화 히스토리 관리 및 문맥 유지
- **GPU 가속**: CUDA를 이용한 음성 변환 고속화
- **오디오 로깅**: 모든 사용자 음성 저장 및 기록

## 🚀 시작하기

### 필수 요구사항

- Python 3.8+
- pip (Python 패키지 관리자)
- OpenRouter API 키
- (선택) NVIDIA GPU (음성 처리 가속화)

### 설치

1. **저장소 클론**
```bash
git clone https://github.com/yourusername/voice_ai_for_kids.git
cd voice_ai_for_kids
```

2. **가상환경 생성 (권장)**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **패키지 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
```bash
cp .env.example .env
# .env 파일을 열어 OpenRouter API 키 입력
# OPENROUTER_API_KEY=your_api_key_here
```

### 빠른 시작

```bash
python main.py
```

프로그램이 시작되면:
1. AI의 첫 인사를 들어보세요
2. **스페이스바를 누르고** 말씀하세요
3. 스페이스바에서 손을 떼면 녹음이 종료됩니다
4. AI가 당신의 말을 이해하고 답변합니다

## ⚙️ 설정

`config.yaml`에서 다양한 옵션을 조정할 수 있습니다:

```yaml
ptt_key: space              # 푸시-투-톡(Push-To-Talk) 키
max_duration: 30            # 최대 녹음 시간 (초)
llm_model: openrouter/elephant-alpha  # LLM 모델
tts_voice: ko-KR-SunHiNeural         # 음성 (한국어 여성)
tts_rate: null              # 음성 속도 (예: "+20%")
tts_pitch: "+30Hz"          # 음성 피치 조정
audio_device: null          # 오디오 장치 (null=기본값)
sample_rate: 16000          # 샘플링 레이트 (Hz)
```

## 📂 프로젝트 구조

```
voice_ai_for_kids/
├── main.py                 # 메인 애플리케이션
├── config.yaml            # 설정 파일
├── .env.example           # 환경변수 예시
├── BOOTSTRAP.md           # AI 성장 컨텍스트
├── requirements.txt       # 의존성 목록
└── src/
    ├── llm.py            # OpenRouter LLM 클라이언트
    ├── stt.py            # 음성 인식 (Whisper)
    ├── tts/               # 텍스트-음성 변환
    │   ├── edge_engine.py
    │   ├── pyttsx3_engine.py
    │   ├── base.py
    │   └── factory.py
    ├── audio.py          # 오디오 녹음
    ├── audio_logger.py   # 오디오 로깅
    ├── memory.py         # 대화 메모리 관리
    ├── ptt.py            # 푸시-투-톡 핸들러
    └── debug.py          # 디버그 로깅
```

## 🔧 주요 모듈

### `src/llm.py`
OpenRouter API를 통해 LLM과 통신하고 대화 컨텍스트를 관리합니다.

### `src/stt.py`
Whisper 모델을 사용하여 음성을 텍스트로 변환합니다.

### `src/tts/`
Edge TTS 또는 pyttsx3를 사용하여 텍스트를 음성으로 변환합니다.
어린이 맞춤형 음성 톤과 피치를 조정합니다.

### `src/memory.py`
대화 히스토리를 저장하고 로드하여 AI가 문맥을 유지하게 합니다.

### `src/audio_logger.py`
모든 사용자 음성과 텍스트를 `logs/` 디렉토리에 기록합니다.

## 🎓 작동 원리

1. **부트스트랩**: `BOOTSTRAP.md`의 컨텍스트를 기반으로 AI가 첫 인사를 생성합니다
2. **사용자 입력**: 스페이스바로 음성을 녹음합니다
3. **음성 인식**: Whisper가 음성을 텍스트로 변환합니다
4. **LLM 처리**: 대화 히스토리와 함께 LLM에 요청을 보냅니다
5. **음성 출력**: TTS가 AI의 응답을 음성으로 생성합니다
6. **메모리 저장**: 대화를 메모리에 저장합니다

## 📝 환경변수

`.env` 파일에 다음을 설정하세요:

```env
OPENROUTER_API_KEY=your_api_key_here
```

[OpenRouter](https://openrouter.ai) 계정을 만들고 API 키를 발급받으세요.

## 🐛 트러블슈팅

### "오디오 장치를 찾을 수 없음"
```bash
# 사용 가능한 오디오 장치 확인
python -c "import sounddevice; print(sounddevice.query_devices())"
# config.yaml의 audio_device에 장치 번호 입력
```

### "STT 실패" 또는 "LLM 오류"
- 네트워크 연결 확인
- API 키가 올바르게 설정되었는지 확인
- API 할당량 초과 여부 확인

### 음성이 너무 높거나 낮음
`config.yaml`에서 `tts_pitch` 값을 조정하세요:
```yaml
tts_pitch: "+50Hz"  # 더 높게
tts_pitch: "-20Hz"  # 더 낮게
```

## 🚀 성능 최적화

### GPU 가속 활성화
NVIDIA GPU가 있다면:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

이를 통해 Whisper와 TTS 처리 속도가 크게 향상됩니다.

## 📜 라이선스

MIT License - 자유롭게 사용, 수정, 배포할 수 있습니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💡 향후 계획

- [ ] 다국어 지원 (영어, 일본어 등)
- [ ] 웹 UI 추가
- [ ] 대화 분석 대시보드
- [ ] 맞춤형 성격 프리셋
- [ ] 로컬 LLM 지원 (Ollama)

## 📧 문의

질문이나 제안이 있으시면 이슈를 열어주세요.

---

**Made with ❤️ for curious kids and their AI friends**
