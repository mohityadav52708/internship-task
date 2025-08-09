from __future__ import annotations

try:
    import pyttsx3  # type: ignore
except Exception:  # noqa: BLE001
    pyttsx3 = None


class Speaker:
    def __init__(self) -> None:
        self._engine = None
        if pyttsx3 is not None:
            try:
                self._engine = pyttsx3.init()
            except Exception:  # noqa: BLE001
                self._engine = None

    def say(self, text: str) -> None:
        if self._engine is not None:
            self._engine.say(text)
            self._engine.runAndWait()
        else:
            print(text)