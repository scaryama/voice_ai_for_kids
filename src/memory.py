from datetime import date
from pathlib import Path

BOOTSTRAP_FILE = "BOOTSTRAP.md"


class ConversationMemory:
    def __init__(self, base_dir: str = "."):
        self._base_dir = Path(base_dir)
        self._path = self._base_dir / f"{date.today().strftime('%Y%m%d')}_MEMORY.md"
        self._bootstrap = self._base_dir / BOOTSTRAP_FILE

    def append(self, role: str, text: str) -> None:
        label = "[아이]" if role == "child" else "[AI]"
        with self._path.open("a", encoding="utf-8") as f:
            f.write(f"{label} {text}\n")

    def load(self) -> str:
        parts = []
        if self._bootstrap.exists():
            parts.append(self._bootstrap.read_text(encoding="utf-8").strip())
        if self._path.exists():
            parts.append(self._path.read_text(encoding="utf-8").strip())
        return "\n".join(parts)
