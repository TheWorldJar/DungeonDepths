from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene


class LicenseEffect(Print):
    """The Game's License Information"""

    def __init__(self, screen):
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
            if event.key_code == ord("b"):  # Press 'b' to go back
                raise NextScene("Start")
            if event.key_code == ord("q"):
                return None
        return event

    def _update(self, frame_no):
        # Draw the top bar
        bar_edge = "=" * (self._screen.width - 2)
        bar_side = "= + ="
        bar_content = "License Information"
        self._screen.print_at(bar_edge, 1, 1, 7, 1)
        self._screen.paint(
            text=bar_side,
            x=1,
            y=2,
            colour_map=[(7, 1, 0), (0, 1, 0), (3, 1, 0), (0, 1, 0), (7, 1, 0)],
        )
        self._screen.print_at(
            bar_content, (self._screen.width - len(bar_content)) // 2, 2, 1, 4
        )
        self._screen.paint(
            text=bar_side,
            x=self._screen.width - 1 - len(bar_side),
            y=2,
            colour_map=[(7, 1, 0), (0, 1, 0), (3, 1, 0), (0, 1, 0), (7, 1, 0)],
        )
        self._screen.print_at(bar_edge, 1, 3, 7, 1)

        # Draw the instructions to go back to the Main Menu
        instruction = "[B]ack to the Main Menu"
        colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
        colour_map += [(7, 1, 0)] * (len(instruction) - 3)
        self._screen.paint(
            text=instruction,
            x=(self._screen.width - len(instruction)) // 2,
            y=self._screen.height - 2,
            colour_map=colour_map,
        )

        return super()._update(frame_no)
