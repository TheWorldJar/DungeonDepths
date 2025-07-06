from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene, StopApplication
from .compositions.topbar import print_top_bar


class StartEffect(Print):
    """The Game's Start Screen"""

    def __init__(self, screen, game_state):
        self.game = game_state
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("s") or event.key_code == ord(
                "S"
            ):  # Press 's' for settings
                self.game.current_scene = "Settings"
                raise NextScene("Settings")
            if event.key_code == ord("q") or event.key_code == ord(
                "Q"
            ):  # Press 'q' to quit
                raise StopApplication("User quit")
            if event.key_code == ord("p") or event.key_code == ord(
                "P"
            ):  # Press 'p' to play
                self.game.current_scene = "Play"
                raise NextScene("Play")
            if event.key_code == ord("m") or event.key_code == ord(
                "M"
            ):  # Press 'm' to manage the player's save
                self.game.current_scene = "Manage"
                raise NextScene("Manage")
            if event.key_code == ord("w") or event.key_code == ord(
                "W"
            ):  # Press 'w' to show warranty information
                self.game.current_scene = "Warranty"
                raise NextScene("Warranty")
            if event.key_code == ord("l") or event.key_code == ord(
                "L"
            ):  # Press 'l' to show license information
                self.game.current_scene = "License"
                raise NextScene("License")
        return event

    def _update(self, frame_no):
        # Draw the top bar
        print_top_bar(self, "Dungeon Depths")

        # Draw navigation options
        nav_options = [
            "[P]lay",
            "[M]anage Save",
            "[S]ettings",
            "[Q]uit",
        ]
        for i, option in enumerate(nav_options):
            colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
            colour_map += [(7, 1, 0)] * (len(option) - 3)
            if i < len(nav_options) // 2:
                x = self.screen.width // 3
                y = i + 5
            else:
                x = (self.screen.width * 2) // 3
                y = (5 - (len(nav_options) // 2)) + i
            self.screen.paint(text=option, x=x, y=y, colour_map=colour_map)

        # Draw social media contacts

        # Draw a copyright statement
        statement = "Copyright (c) 2025, TheWorldJar"
        self.screen.print_at(
            statement,
            (self.screen.width - len(statement)) // 2,
            self.screen.height - 4,
            3,
            4,
        )
        statement = "[L]icense"
        colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
        colour_map += [(7, 1, 0)] * (len(statement) - 3)
        self.screen.paint(
            text=statement,
            x=(self.screen.width // 2) - len(statement) - 1,
            y=self.screen.height - 3,
            colour_map=colour_map,
        )
        statement = "[W]arranty"
        colour_map = [(1, 1, 0), (3, 4, 0), (1, 1, 0)]
        colour_map += [(7, 1, 0)] * (len(statement) - 3)
        self.screen.paint(
            text=statement,
            x=(self.screen.width // 2) + 1,
            y=self.screen.height - 3,
            colour_map=colour_map,
        )
