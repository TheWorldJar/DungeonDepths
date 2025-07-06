from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.exceptions import NextScene

from .compositions.screensize import print_screen_size, MIN_WIDTH, MIN_HEIGHT


class SettingsEffect(Print):
    """The Game's Setting Screen"""

    def __init__(self, screen, game_state):
        self.game = game_state
        super().__init__(
            screen=screen, renderer=FigletText("Settings", font="big"), y=2
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("b") or event.key_code == ord(
                "B"
            ):  # Press 'b' to go back
                self.game.current_scene = "Start"
                raise NextScene("Start")
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None
        return event

    def _update(self, frame_no):
        if self.screen.width < MIN_WIDTH or self.screen.height < MIN_HEIGHT:
            print_screen_size(self)
        else:
            return super()._update(frame_no)
