#!/bin/bash
set -e

if [ ! -f .env ]; then
    echo "[오류] .env 파일이 없습니다. .env.example 을 복사하여 API 키를 설정해주세요."
    exit 1
fi

# Mac 호환성: PortAudio 설치 (관리자 권한 전에만 실행, 일반 권한에서)
# SUDO_USER가 없으면 일반 사용자 권한 (재실행되지 않은 상태)
if [[ "$OSTYPE" == "darwin"* ]] && [ -z "$SUDO_USER" ]; then
    echo "[Mac 감지] PortAudio 설치 확인 중..."
    if ! command -v brew &> /dev/null; then
        echo "[오류] Homebrew가 설치되어 있지 않습니다. 다음 명령어를 실행하세요:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi
    if ! brew list portaudio &> /dev/null; then
        echo "[설치] PortAudio 설치 중..."
        brew install portaudio
    fi
fi

# Mac에서 처음 실행할 때 관리자 권한으로 재실행 (keyboard 라이브러리가 필요)
if [[ "$OSTYPE" == "darwin"* ]] && [ "$EUID" -ne 0 ]; then
    echo "[알림] Mac에서 keyboard 입력을 감지하려면 관리자 권한이 필요합니다."
    sudo bash "$0" "$@"
    exit $?
fi

# venv 없으면 생성
if [ ! -f .venv/bin/python ]; then
    echo "[설치] 가상환경 생성 중..."
    python3 -m venv .venv
fi

# 의존성 설치
echo "[설치] 의존성 확인 중..."
.venv/bin/pip install -q -r requirements.txt

echo "KidVoice AI 시작 중..."
export PYTHONUTF8=1
.venv/bin/python main.py "$@"
