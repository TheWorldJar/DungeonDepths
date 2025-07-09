import os
import json

from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene, StopApplication
from .compositions.topbar import print_top_bar
from .compositions.screensize import print_screen_size, MIN_WIDTH, MIN_HEIGHT


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
                save = self.check_save()
                if save is not None:
                    self.load_save(save)
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
        if self.screen.width < MIN_WIDTH or self.screen.height < MIN_HEIGHT:
            print_screen_size(self)
        else:
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

    def check_save(self) -> str:
        save_path = os.path.realpath("./save")
        save_file = os.path.realpath("./save/save.json")
        # If there is no save file directory, create it.
        if not os.path.exists(save_path) or not os.path.isdir(save_path):
            os.makedirs(save_path)

        # If there is a save.json file, try to load it.
        if os.path.exists(save_file) and os.path.isfile(save_file):
            try:
                json.loads(save_file)
            except ValueError:
                return None
            return save_file
        # Otherwise, create a blank save file.
        else:
            data = {"characters": [], "inventory": [], "slots": 2}
            with open(save_file, "w") as s:
                json.dump(data, s, indent=4)
            return None

    def load_save(self, save_file):
        # Placeholder
        pass
