from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError
from scenes.start_screen import StartEffect
from scenes.settings import SettingsEffect


def demo(screen, scene):
    start_scene = Scene([StartEffect(screen)], -1, name="Start")
    settings_scene = Scene([SettingsEffect(screen)], -1, name="Settings")
    screen.play([start_scene, settings_scene], stop_on_resize=True, start_scene=scene)


def main():
    """The program's entry point"""
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, arguments=[last_scene])
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
