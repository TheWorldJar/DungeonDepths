from asciimatics.effects import Print
from asciimatics.screen import Screen


def print_vertical_bar(
    source: Print,
    x: int,
    end_y: int,
    start_y=4,
    char="|",
    colour=Screen.COLOUR_WHITE,
    attr=Screen.A_BOLD,
    bg=Screen.COLOUR_BLACK,
):
    """
    Helper function to draw a vertical bar of the specified character at a specified x and y coordinate.
    By default, y = 4 to start drawing below the top bar present on most screens.
    """
    while start_y < end_y:
        source.screen.print_at(
            text=char, x=x, y=start_y, colour=colour, attr=attr, bg=bg
        )
        start_y += 1
