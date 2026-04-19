import keyboard


class PTTHandler:
    def __init__(self, config: dict):
        self._key = config.get("ptt_key", "space")

    def wait_for_press(self) -> bool:
        keyboard.wait(self._key, suppress=True)
        return True

    def is_pressed(self) -> bool:
        return keyboard.is_pressed(self._key)
