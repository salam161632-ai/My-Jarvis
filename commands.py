"""Command handling for Jarvis.

This module has no audio dependencies, so it can be tested with plain text.
`handle(text)` returns a tuple: (reply, should_exit).
"""

from __future__ import annotations

import datetime
import random
import re
import urllib.parse
import webbrowser

SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "whatsapp": "https://web.whatsapp.com",
    "wikipedia": "https://www.wikipedia.org",
}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are only 10 kinds of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: can I join you?",
]

EXIT_WORDS = ("exit", "quit", "goodbye", "bye", "stop listening", "বিদায়", "বন্ধ করো")
TIME_WORDS = ("what time", "the time", "time is it", "সময়")
DATE_WORDS = ("what date", "today's date", "what day", "the date", "তারিখ")

HELP_TEXT = (
    "You can ask me: what time it is, today's date, open youtube, "
    "search for something, who is someone, tell me a joke, or say goodbye."
)


def handle(text: str) -> tuple[str, bool]:
    """Turn a spoken or typed command into (reply, should_exit)."""
    text = text.lower().strip()
    if not text:
        return "I did not catch that.", False

    if any(word in text for word in EXIT_WORDS):
        return "Goodbye!", True

    if any(word in text for word in TIME_WORDS):
        return datetime.datetime.now().strftime("It is %I:%M %p."), False

    if any(word in text for word in DATE_WORDS):
        return datetime.datetime.now().strftime("Today is %A, %d %B %Y."), False

    match = re.match(r"^(?:open|launch)\s+(.+)$", text)
    if match:
        return _open_site(match.group(1).strip()), False

    match = re.match(r"^(?:search|google)(?:\s+for)?\s+(.+)$", text)
    if match:
        return _web_search(match.group(1).strip()), False

    match = re.match(r"^(?:who is|who was|what is|tell me about|wikipedia)\s+(.+)$", text)
    if match:
        return _wikipedia_summary(match.group(1).strip()), False

    if "joke" in text:
        return random.choice(JOKES), False

    if re.search(r"\b(hello|hi|hey)\b", text) or "নমস্কার" in text or "হ্যালো" in text:
        return "Hello! How can I help you?", False

    if "help" in text:
        return HELP_TEXT, False

    return "Sorry, I don't know that command yet. Say help to hear what I can do.", False


def _open_site(name: str) -> str:
    url = SITES.get(name)
    if url is None:
        return f"I don't know the site {name}. Add it to the SITES dictionary in commands.py."
    webbrowser.open(url)
    return f"Opening {name}."


def _web_search(query: str) -> str:
    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
    return f"Searching the web for {query}."


def _wikipedia_summary(topic: str) -> str:
    try:
        import wikipedia
    except ImportError:
        return "The wikipedia package is not installed. Run pip install wikipedia."

    try:
        return wikipedia.summary(topic, sentences=2)
    except wikipedia.exceptions.DisambiguationError as error:
        options = ", ".join(error.options[:3])
        return f"That is ambiguous. Did you mean {options}?"
    except wikipedia.exceptions.PageError:
        return f"I could not find anything about {topic}."
    except Exception:
        return "I could not reach Wikipedia right now."
