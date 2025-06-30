from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.exceptions import NextScene, StopApplication


class StartEffect(Print):
    """The Game's Start Screen"""

    def __init__(self, screen):
        super().__init__(
            screen=screen, renderer=FigletText("Start Screen", font="big"), y=2
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("s"):  # Press 's' for settings
                raise NextScene("Settings")
            elif event.key_code == ord("q"):  # Press 'q' to quit
                raise StopApplication("User quit")
        return event
