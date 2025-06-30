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
            elif event.key_code == ord("q"):  # Press 'q' to quit
                raise StopApplication("User quit")
        return event

    def _update(self, frame_no):
        # Draw the top bar
        bar_edge = "=" * (self.screen.width - 2)
        bar_side = "= + ="
        bar_content = "Dungeon Depths"
        self.screen.print_at(bar_edge, 1, 1)
        self.screen.print_at(bar_side, 1, 2)
        self.screen.print_at(
            bar_content, (self._screen.width - len(bar_content)) // 2, 2
        )
        self.screen.print_at(bar_side, self._screen.width - 1 - len(bar_side), 2)
        self.screen.print_at(bar_edge, 1, 3)

        # Draw navigation options
        nav_options = "[S]ettings [Q]uit"
        x = (self.screen.width - len(nav_options)) // 2
        self.screen.print_at(nav_options, x, 5)

        return super()._update(frame_no)
