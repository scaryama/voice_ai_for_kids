import os


class DebugLogger:
    def __init__(self):
        self._enabled = os.environ.get("DEBUG", "0") == "1"

    def log(self, message: str) -> None:
        if self._enabled:
            print(message, flush=True)

    def log_status(self, message: str) -> None:
        self.log(f"[{message}]")

    def log_error(self, message: str) -> None:
        self.log(f"[오류] {message}")

    def log_conversation(self, role: str, text: str) -> None:
        self.log(f"[{role}] {text}")
