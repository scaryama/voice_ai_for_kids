@echo off
chcp 65001 >nul

if not exist .env (
    echo [오류] .env 파일이 없습니다. .env.example 을 복사하여 API 키를 설정해주세요.
    pause
    exit /b 1
)

:: venv 없으면 생성
if not exist .venv\Scripts\python.exe (
    echo [설치] 가상환경 생성 중...
    python -m venv .venv
    if errorlevel 1 (
        echo [오류] venv 생성 실패. Python 3.10 이상이 설치되어 있는지 확인하세요.
        pause
        exit /b 1
    )
)

:: 의존성 설치 (requirements 변경 시 재설치)
echo [설치] 의존성 확인 중...
.venv\Scripts\pip install -q -r requirements.txt

echo KidVoice AI 시작 중...
set PYTHONUTF8=1
.venv\Scripts\python main.py %*
