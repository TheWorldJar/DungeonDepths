from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene, StopApplication


class StartEffect(Print):
    """The Game's Start Screen"""

    def __init__(self, screen):
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("s"):  # Press 's' for settings
                raise NextScene("Settings")
            if event.key_code == ord("q"):  # Press 'q' to quit
                raise StopApplication("User quit")
            if event.key_code == ord("p"):  # Press 'p' to play
                raise NextScene("Play")
            if event.key_code == ord("m"):  # Press 'm' to manage the player's save
                raise NextScene("Manage")
            if event.key_code == ord("w"):  # Press 'w' to show warranty information
                raise NextScene("Warranty")
            if event.key_code == ord("l"):  # Press 'l' to show license information
                raise NextScene("License")
        return event

    def _update(self, frame_no):
        # Draw the top bar
        bar_edge = "=" * (self._screen.width - 2)
        bar_side = "= + ="
        bar_content = "Dungeon Depths"
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

        # Draw navigation options
        nav_options = ["[P]lay", "[M]anage Save", "[S]ettings", "[Q]uit"]
        for i, option in enumerate(nav_options):
            x = (self._screen.width - len(option)) // 2
            colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
            colour_map += [(7, 1, 0)] * (len(option) - 3)
            self._screen.paint(text=option, x=x, y=i + 5, colour_map=colour_map)

        # Draw social media contacts

        # Draw a copyright statement
        statement = "Copyright (c) 2025, TheWorldJar"
        self._screen.print_at(
            statement,
            (self._screen.width - len(statement)) // 2,
            self._screen.height - 4,
            3,
            4,
        )
        statement = "[L]icense"
        colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
        colour_map += [(7, 1, 0)] * (len(statement) - 3)
        self._screen.paint(
            text=statement,
            x=(self._screen.width // 2) - len(statement) - 1,
            y=self._screen.height - 3,
            colour_map=colour_map,
        )
        statement = "[W]arranty"
        colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
        colour_map += [(7, 1, 0)] * (len(statement) - 3)
        self._screen.paint(
            text=statement,
            x=(self._screen.width // 2) + 1,
            y=self._screen.height - 3,
            colour_map=colour_map,
        )
