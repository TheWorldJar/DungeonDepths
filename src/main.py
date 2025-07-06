import sys

from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError

from game import GameState

from scenes.start_screen import StartEffect
from scenes.settings import SettingsEffect
from scenes.play import PlayEffect
from scenes.manage_save import ManageEffect
from scenes.warranty import WarrantyEffect
from scenes.license import LicenseEffect


# 180x35
def screens(screen, scene, game_state):
    """The game's screen and its scenes"""
    start_scene = Scene([StartEffect(screen, game_state)], -1, name="Start")
    settings_scene = Scene([SettingsEffect(screen, game_state)], -1, name="Settings")
    play_scene = Scene([PlayEffect(screen, game_state)], -1, name="Play")
    manage_scene = Scene([ManageEffect(screen, game_state)], -1, name="Manage")
    warranty_scene = Scene([WarrantyEffect(screen, game_state)], -1, name="Warranty")
    license_scene = Scene([LicenseEffect(screen, game_state)], -1, name="License")
    screen.play(
        [
            start_scene,
            settings_scene,
            play_scene,
            manage_scene,
            warranty_scene,
            license_scene,
        ],
        stop_on_resize=True,
        start_scene=scene,
    )


def main():
    """The program's entry point"""
    last_scene = None
    game = GameState()
    while True:
        try:
            Screen.wrapper(screens, arguments=[last_scene, game])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
