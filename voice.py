"""Speech input and output for Jarvis."""

from __future__ import annotations


class Speaker:
    """Offline text-to-speech using pyttsx3."""

    def __init__(self, rate: int = 175) -> None:
        import pyttsx3

        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)

    def say(self, text: str) -> None:
        print(f"Jarvis: {text}")
        self._engine.say(text)
        self._engine.runAndWait()


class Listener:
    """Microphone input using SpeechRecognition (Google Web Speech API)."""

    def __init__(self, language: str = "en-IN") -> None:
        import speech_recognition as sr

        self._sr = sr
        self._language = language
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        with self._microphone as source:
            print("Calibrating for background noise...")
            self._recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen(self, timeout: int = 5, phrase_limit: int = 8) -> str:
        """Return the recognised text in lower case, or '' if nothing was understood."""
        with self._microphone as source:
            try:
                audio = self._recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            except self._sr.WaitTimeoutError:
                return ""

        try:
            heard = self._recognizer.recognize_google(audio, language=self._language)
        except self._sr.UnknownValueError:
            return ""
        except self._sr.RequestError:
            print("Speech service unavailable. Check your internet connection.")
            return ""

        heard = heard.lower()
        print(f"You: {heard}")
        return heard


class TextListener:
    """Keyboard fallback when no microphone is available (--text mode)."""

    def listen(self, timeout: int = 0, phrase_limit: int = 0) -> str:
        try:
            return input("You: ").strip().lower()
        except EOFError:
            return "exit"
