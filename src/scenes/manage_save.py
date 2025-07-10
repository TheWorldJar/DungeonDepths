from asciimatics.effects import Print
from asciimatics.renderers import FigletText


class ManageEffect(Print):
    """The Game's Manage Savegame Screen"""

    def __init__(self, screen, game_state):
        self.game = game_state

        # Placeholder
        super().__init__(
            screen=screen, renderer=FigletText("Manage Save", font="big"), y=2
        )
