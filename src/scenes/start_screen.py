from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.screen import Screen

from src.const import (
    MIN_SCREEN_HEIGHT,
    MIN_SCREEN_WIDTH,
    SETTINGS_SCENE,
    PLAY_SCENE,
    MANAGE_SAVE_SCENE,
    WARRANTY_SCENE,
    LICENSE_SCENE,
)
from src.game import GameState

from src.save import check_save, load_save, set_save_status

from src.scenes.compositions.topbar import print_top_bar
from src.scenes.compositions.screensize import print_screen_size


class StartEffect(Print):
    """The Game's Start Screen"""

    def __init__(self, screen, game_state: GameState):
        self.game = game_state

        # This is only for initilization.
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code in (ord("s"), ord("S")):
                self.game.set_scene(SETTINGS_SCENE)
                raise NextScene(SETTINGS_SCENE)
            if event.key_code in (ord("q"), ord("Q")):
                raise StopApplication("User quit")
            if event.key_code in (ord("p"), ord("P")):
                save = check_save(self.game)
                if save is not None:
                    load_save(self.game, save)
                self.game.set_scene(PLAY_SCENE)
                raise NextScene(PLAY_SCENE)
            if event.key_code in (ord("m"), ord("M")):
                set_save_status(self.game)
                self.game.set_scene(MANAGE_SAVE_SCENE)
                raise NextScene(MANAGE_SAVE_SCENE)
            if event.key_code in (ord("w"), ord("W")):
                self.game.set_scene(WARRANTY_SCENE)
                raise NextScene(WARRANTY_SCENE)
            if event.key_code in (ord("l"), ord("L")):
                self.game.set_scene(LICENSE_SCENE)
                raise NextScene(LICENSE_SCENE)
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
        return event

    def _update(self, frame_no):
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
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
                colour_map = [
                    (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                    (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                    (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                ]
                colour_map += [
                    (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
                ] * (
                    len(option) - 3
                )  # The first 3 characters have already been defined above.

                # Options a split into 2 collumns.
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
                text=statement,
                x=(self.screen.width - len(statement)) // 2,
                y=self.screen.height - 4,
                colour=Screen.COLOUR_YELLOW,
                attr=Screen.A_UNDERLINE,
            )

            # We reuse statement to make position calculations easier.
            statement = "[L]icense"
            colour_map = [
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            ]
            colour_map += [
                (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            ] * (
                len(statement) - 3
            )  # The first 3 characters have already been defined above.
            self.screen.paint(
                text=statement,
                x=(self.screen.width // 2) - len(statement) - 1,
                y=self.screen.height - 3,
                colour_map=colour_map,
            )
            statement = "[W]arranty"
            colour_map = [
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            ]
            colour_map += [
                (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            ] * (
                len(statement) - 3
            )  # The first 3 characters have already been defined above.
            self.screen.paint(
                text=statement,
                x=(self.screen.width // 2) + 1,
                y=self.screen.height - 3,
                colour_map=colour_map,
            )
