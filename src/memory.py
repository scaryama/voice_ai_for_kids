from datetime import date
from pathlib import Path

BOOTSTRAP_FILE = "BOOTSTRAP.md"


class ConversationMemory:
    def __init__(self, base_dir: str = "memorys"):
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(exist_ok=True)
        self._path = self._base_dir / f"{date.today().strftime('%Y%m%d')}_MEMORY.md"
        self._bootstrap = Path(BOOTSTRAP_FILE)

    def append(self, role: str, text: str) -> None:
        label = "[사용자]" if role == "child" else "[AI]"
        with self._path.open("a", encoding="utf-8") as f:
            f.write(f"{label} {text}\n")

    def load(self) -> str:
        """순수 대화 기록만 반환 (BOOTSTRAP은 SYSTEM_PROMPT에 포함되어 있음)"""
        if self._path.exists():
            return self._path.read_text(encoding="utf-8").strip()
        return ""
