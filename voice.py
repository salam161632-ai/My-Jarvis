"""Speech input and output for Jarvis with Bengali Support."""

from __future__ import annotations
import speech_recognition as sr
from gtts import gTTS
import os
import pygame

class Speaker:
    """Online text-to-speech using gTTS for clear Bengali voice."""
    def __init__(self):
        pass

    def say(self, text: str) -> None:
        print(f"Jarvis: {text}")
        tts = gTTS(text=text, lang='bn', slow=False)
        tts.save("response.mp3")
        
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove("response.mp3")

class Listener:
    """Microphone input using SpeechRecognition for Bengali (bn-BD)."""
    def __init__(self, language: str = "bn-BD") -> None:
        self._sr = sr
        self._language = language
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        with self._microphone as source:
            print("Calibrating for background noise...")
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)

    def listen(self, timeout: int = 5, phrase_limit: int = 8) -> str:
        """Return the recognised text in lower case, or '' if timeout/error."""
        with self._microphone as source:
            try:
                audio = self._recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            except self._sr.WaitTimeoutError:
                return ""
        
        try:
            return self._recognizer.recognize_google(audio, language=self._language)
        except self._sr.UnknownValueError:
            return ""
        except self._sr.RequestError:
            return ""
            
