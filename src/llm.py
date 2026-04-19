import os
import re
from typing import Optional
from openai import OpenAI

SYSTEM_PROMPT = (
    "emoji 사용 금지."
    "너는 어린이의 친한 친구야. "
    "5살 아이가 이해할 수 있는 쉽고 재미있는 말로 대답해줘. "
    "답변은 한글로 20~50자 이내로 짧게 해줘."
)


class LLMClient:
    def __init__(self, config: dict):
        self._model = config.get("llm_model", "openrouter/elephant-alpha")
        self._client = OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
        )

    def _sanitize_for_tts(self, text: str) -> str:
        """TTS에 안전한 문자만 유지: 한글, 영어, 숫자, 기본 기호"""
        # 화이트리스트: 한글, 영어, 숫자, 공백, 기본 문장 기호
        safe_pattern = re.compile(r"[^가-힣a-zA-Z0-9\s\.\!\?\,\-\'\"]")
        return safe_pattern.sub(r"", text).strip()

    def _parse_history(self, history_text: str) -> list[dict]:
        messages = []
        for line in history_text.strip().splitlines():
            line = line.strip()
            if line.startswith("[아이]"):
                messages.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith("[AI]"):
                messages.append({"role": "assistant", "content": line[4:].strip()})
        return messages

    def chat(self, user_text: str, history_text: str = "") -> Optional[str]:
        history = self._parse_history(history_text)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=200,
        )
        text = response.choices[0].message.content.strip()
        return self._sanitize_for_tts(text)
