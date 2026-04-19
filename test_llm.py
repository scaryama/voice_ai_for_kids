"""LLM 최소 테스트 — Bootstrap 영향도 확인"""
import time
import yaml
from dotenv import load_dotenv

load_dotenv()

from src.llm import LLMClient, SYSTEM_PROMPT
from src.memory import ConversationMemory

# 설정 로드
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print("LLM 모델 초기화 중...")
llm = LLMClient(config)
print(f"✓ 모델: {config.get('llm_model', 'openrouter/elephant-alpha')}\n")

print("📋 SYSTEM_PROMPT:")
print(f"{SYSTEM_PROMPT}\n")

# 테스트 1: Bootstrap + Memory 로드
print("=" * 60)
print("테스트 1: Bootstrap + Memory 로드")
print("=" * 60)
memory = ConversationMemory()
history = memory.load()
print(f"✓ Bootstrap + Memory 로드 완료")
print(f"   히스토리 길이: {len(history)} 글자\n")

# 테스트 2: Bootstrap 없이 질문 (비교 대상)
print("=" * 60)
print("테스트 2: Bootstrap 없이 질문")
print("=" * 60)
print("질문: '안녕하세요, 뭐 하고 있어요?'")
t0 = time.time()
response_no_bootstrap = llm.chat("한국말로 대화를 시작해줘. 짧게 인사하고 궁금한걸 물어봐.", history="")
elapsed = time.time() - t0
print(f"응답: {response_no_bootstrap}")
print(f"소요시간: {elapsed:.1f}초\n")

# 테스트 3: Bootstrap + Memory 포함해서 같은 질문
print("=" * 60)
print("테스트 3: Bootstrap + Memory 포함해서 질문")
print("=" * 60)
print("질문: '안녕하세요, 뭐 하고 있어요?'")
t0 = time.time()
response_with_bootstrap = llm.chat("한국말로 대화를 시작해줘. 짧게 인사하고 궁금한걸 물어봐.", history)
elapsed = time.time() - t0
print(f"응답: {response_with_bootstrap}")
print(f"소요시간: {elapsed:.1f}초\n")

# 테스트 4: Bootstrap 영향도 비교
print("=" * 60)
print("테스트 4: Bootstrap 영향도 비교")
print("=" * 60)
if response_with_bootstrap != response_no_bootstrap:
    print("✓ Bootstrap이 응답에 영향을 미침 (응답이 다름)")
    print(f"  - Bootstrap 없음: {response_no_bootstrap}")
    print(f"  - Bootstrap 있음: {response_with_bootstrap}")
else:
    print("ℹ 동일한 응답 (Bootstrap 영향이 작거나 같은 맥락)")
    print(f"  응답: {response_with_bootstrap}")
print()

# 테스트 5: main.py 패턴 - 첫 인사 (Bootstrap+Memory 포함)
print("=" * 60)
print("테스트 5: 첫 인사 생성 (main.py 패턴)")
print("=" * 60)
print("질문: '한국말로 대화를 시작해줘. 짧게 인사하고 궁금한걸 물어봐.'")
t0 = time.time()
greeting = llm.chat("한국말로 대화를 시작해줘. 짧게 인사하고 궁금한걸 물어봐.", history)
elapsed = time.time() - t0
print(f"응답: {greeting}")
print(f"소요시간: {elapsed:.1f}초\n")

# 테스트 6: main.py 패턴 - 일반 질문 (Bootstrap+Memory 포함)
print("=" * 60)
print("테스트 6: 일반 질문 (main.py 패턴)")
print("=" * 60)
print("질문: '공룡은 뭐야?'")
t0 = time.time()
answer = llm.chat("공룡은 뭐야?", history)
elapsed = time.time() - t0
print(f"응답: {answer}")
print(f"소요시간: {elapsed:.1f}초\n")

print("=" * 60)
print("✅ 모든 테스트 완료")
print("=" * 60)
