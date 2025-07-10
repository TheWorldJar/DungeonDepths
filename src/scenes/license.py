from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen

from src.const import MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT

from src.scenes.compositions.topbar import print_top_bar
from src.scenes.compositions.screensize import print_screen_size


class LicenseEffect(Print):
    """The Game's License Information"""

    def __init__(self, screen, game_state):
        self.game = game_state
        preamble = """
                      GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 The precise terms and conditions for copying, distribution and
 modification can be found in the LICENSE file in the root of this project."""
        super().__init__(
            screen=screen,
            renderer=SpeechBubble(preamble),
            y=5,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("b") or event.key_code == ord(
                "B"
            ):  # Press 'b' to go back
                self.game.current_scene = "Start"
                raise NextScene("Start")
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None  # Disables global exit on this screen.
        return event

    def _update(self, frame_no):
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
            print_screen_size(self)
        else:
            print_top_bar(self, "License")

            # Draw the instructions to go back to the Main Menu
            instruction = "[B]ack to the Main Menu"
            colour_map = [
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            ]
            colour_map += [
                (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            ] * (
                len(instruction) - 3
            )  # The first 3 characters are already defined above.
            self._screen.paint(
                text=instruction,
                x=(self._screen.width - len(instruction)) // 2,
                y=self._screen.height - 2,
                colour_map=colour_map,
            )

            return super()._update(frame_no)
