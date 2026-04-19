#!/bin/bash
set -e

if [ ! -f .env ]; then
    echo "[오류] .env 파일이 없습니다. .env.example 을 복사하여 API 키를 설정해주세요."
    exit 1
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
