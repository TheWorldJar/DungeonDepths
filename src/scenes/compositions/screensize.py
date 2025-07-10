from asciimatics.effects import Print
from asciimatics.screen import Screen

from src.const import MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT


def print_screen_size(source: Print):
    t1 = "Terminal too small!"
    t2 = f"Minimum: {MIN_SCREEN_WIDTH}x{MIN_SCREEN_HEIGHT}"
    t3 = f"Current: {source.screen.width}x{source.screen.height}"
    source.screen.print_at(
        text=t1,
        x=(source.screen.width - len(t1)) // 2,
        y=1,
        colour=Screen.COLOUR_RED,
        attr=Screen.A_UNDERLINE,
    )
    source.screen.print_at(
        text=t2,
        x=(source.screen.width - len(t2)) // 2,
        y=2,
        colour=Screen.COLOUR_RED,
        attr=Screen.A_UNDERLINE,
    )
    source.screen.print_at(
        text=t3,
        x=(source.screen.width - len(t3)) // 2,
        y=3,
        colour=Screen.COLOUR_RED,
        attr=Screen.A_UNDERLINE,
    )
