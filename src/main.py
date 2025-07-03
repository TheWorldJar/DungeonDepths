import sys
import time

from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError

from scenes.start_screen import StartEffect
from scenes.settings import SettingsEffect
from scenes.play import PlayEffect
from scenes.manage_save import ManageEffect
from scenes.warranty import WarrantyEffect
from scenes.license import LicenseEffect


def screen_init(screen, scene):
    """Initializes th game's screen and its scenes"""
    start_scene = Scene([StartEffect(screen)], -1, name="Start")
    settings_scene = Scene([SettingsEffect(screen)], -1, name="Settings")
    play_scene = Scene([PlayEffect(screen)], -1, name="Play")
    manage_scene = Scene([ManageEffect(screen)], -1, name="Manage")
    warranty_scene = Scene([WarrantyEffect(screen)], -1, name="Warranty")
    license_scene = Scene([LicenseEffect(screen)], -1, name="License")
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
    last_time = time.perf_counter()
    while True:
        if time.perf_counter() - last_time > 1.0 / 20:
            last_time = time.perf_counter
            try:
                Screen.wrapper(screen_init, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene


if __name__ == "__main__":
    main()
