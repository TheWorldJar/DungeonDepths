from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen

from src.const import MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH, START_SCENE

from .compositions.screensize import print_screen_size


class SettingsEffect(Print):
    """The Game's Setting Screen"""

    def __init__(self, screen, game_state):
        self.game = game_state

        # Placeholder
        super().__init__(
            screen=screen, renderer=FigletText("Settings", font="big"), y=2
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code in (ord("b"), ord("B")):  # Press 'b' to go back
                self.game.current_scene = START_SCENE
                raise NextScene(START_SCENE)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
        return event

    def _update(self, frame_no):
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
            print_screen_size(self)
        else:
            return super()._update(frame_no)
