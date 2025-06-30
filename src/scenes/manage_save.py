from asciimatics.effects import Print
from asciimatics.renderers import FigletText


class ManageEffect(Print):
    """The Game's Setting Screen"""

    def __init__(self, screen):
        super().__init__(
            screen=screen, renderer=FigletText("Manage Save", font="big"), y=2
        )
