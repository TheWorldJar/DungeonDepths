import sys
import asyncio

from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError

from src.game import GameState
from src.const import (
    START_SCENE,
    SETTINGS_SCENE,
    PLAY_SCENE,
    MANAGE_SAVE_SCENE,
    WARRANTY_SCENE,
    LICENSE_SCENE,
)

from src.scenes.start_screen import StartEffect
from src.scenes.settings import SettingsEffect
from src.scenes.play import PlayEffect
from src.scenes.manage_save import ManageEffect
from src.scenes.warranty import WarrantyEffect
from src.scenes.license import LicenseEffect


def screens(screen, scene, game_state):
    """The game's screen and its scenes"""
    start_scene = Scene([StartEffect(screen, game_state)], -1, name=START_SCENE)
    settings_scene = Scene(
        [SettingsEffect(screen, game_state)], -1, name=SETTINGS_SCENE
    )
    play_scene = Scene([PlayEffect(screen, game_state)], -1, name=PLAY_SCENE)
    manage_scene = Scene([ManageEffect(screen, game_state)], -1, name=MANAGE_SAVE_SCENE)
    warranty_scene = Scene(
        [WarrantyEffect(screen, game_state)], -1, name=WARRANTY_SCENE
    )
    license_scene = Scene([LicenseEffect(screen, game_state)], -1, name=LICENSE_SCENE)
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


async def main():
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
    asyncio.run(main())
