from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene


class PlayEffect(Print):
    """The Game's Play Screen"""

    def __init__(self, screen):
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None
            if event.key_code == ord("b") or event.key_code == ord("B"):
                raise NextScene("Start")
        return event
