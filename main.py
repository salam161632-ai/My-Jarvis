"""Entry point for My-Jarvis.

Examples:
    python main.py                      # voice mode, say "Jarvis, what time is it"
    python main.py --lang bn-BD         # Bengali speech recognition
    python main.py --text               # type commands instead of speaking
"""

from __future__ import annotations

import argparse

from jarvis.commands import handle


def extract_command(heard: str, wake_word: str) -> str | None:
    """Return the text after the wake word, or None if the wake word was not said."""
    if wake_word not in heard:
        return None
    return heard.split(wake_word, 1)[1].strip(" ,.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="My-Jarvis voice assistant")
    parser.add_argument("--wake-word", default="jarvis", help="word that activates the assistant")
    parser.add_argument("--lang", default="en-IN", help="speech recognition language, e.g. en-US, bn-BD")
    parser.add_argument("--text", action="store_true", help="type commands instead of using the microphone")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    wake_word = args.wake_word.lower()

    if args.text:
        from jarvis.voice import TextListener

        listener = TextListener()
        speaker = None
    else:
        from jarvis.voice import Listener, Speaker

        listener = Listener(args.lang)
        speaker = Speaker()

    def say(text: str) -> None:
        if speaker:
            speaker.say(text)
        else:
            print(f"Jarvis: {text}")

    say("Jarvis is ready." if args.text else f"Jarvis is ready. Say {wake_word} to wake me up.")

    while True:
        heard = listener.listen()
        if not heard:
            continue

        if args.text:
            command = heard
        else:
            command = extract_command(heard, wake_word)
            if command is None:
                continue
            if command == "":
                say("Yes?")
                command = listener.listen(timeout=6)
                if not command:
                    continue

        reply, should_exit = handle(command)
        say(reply)
        if should_exit:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
