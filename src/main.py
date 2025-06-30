from asciimatics.screen import Screen
from asciimatics.scene import Scene
from scenes.start_screen import StartEffect
from scenes.settings import SettingsEffect


def demo(screen):
    start_scene = Scene([StartEffect(screen)], -1, name="Start")
    settings_scene = Scene([SettingsEffect(screen)], -1, name="Settings")
    screen.play(
        [start_scene, settings_scene], stop_on_resize=True, start_scene=start_scene
    )


def main():
    Screen.wrapper(demo)


if __name__ == "__main__":
    main()
