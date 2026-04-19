import pyttsx3

ERROR_MESSAGE = "다시 한번 말해주세요"


class TTSEngine:
    def __init__(self, config: dict):
        self._voice_id = config.get("tts_voice")

    def _speak(self, text: str) -> None:
        engine = pyttsx3.init()
        if self._voice_id:
            engine.setProperty("voice", self._voice_id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    def speak(self, text: str) -> None:
        self._speak(text)

    def speak_error(self) -> None:
        self._speak(ERROR_MESSAGE)
