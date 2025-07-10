from asciimatics.effects import Print
from asciimatics.screen import Screen


def print_top_bar(source: Print, content: str):
    """
    Helper function to draw the game's top bar
    The top bar is the same across many screens.
    """
    bar_edge = "=" * (source.screen.width - 2)
    bar_side = "= + ="
    bar_content = content
    source.screen.print_at(
        text=bar_edge, x=1, y=1, colour=Screen.COLOUR_WHITE, attr=Screen.A_BOLD
    )
    source.screen.paint(
        text=bar_side,
        x=1,
        y=2,
        colour_map=[
            (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK),
            (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK),
            (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        ],
    )
    source.screen.print_at(
        text=bar_content,
        x=(source.screen.width - len(bar_content)) // 2,
        y=2,
        colour=Screen.COLOUR_RED,
        attr=Screen.A_UNDERLINE,
    )
    source.screen.paint(
        text=bar_side,
        x=source.screen.width - 1 - len(bar_side),
        y=2,
        colour_map=[
            (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK),
            (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK),
            (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        ],
    )
    source.screen.print_at(
        text=bar_edge, x=1, y=3, colour=Screen.COLOUR_WHITE, attr=Screen.A_BOLD
    )
