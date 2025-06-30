from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.exceptions import NextScene, StopApplication


class StartEffect(Print):
    def __init__(self, screen):
        super().__init__(
            screen=screen, renderer=FigletText("Start Screen", font="big"), y=2
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("s"):  # Press 's' for settings
                raise NextScene("Settings")
            elif event.key_code == ord("q"):  # Press 'q' to quit
                raise StopApplication("User quit")
        return event


class SettingsEffect(Print):
    def __init__(self, screen):
        super().__init__(
            screen=screen, renderer=FigletText("Settings", font="big"), y=2
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code == ord("b"):  # Press 'b' to go back
                raise NextScene("Start")
        return event


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
