from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from .compositions.topbar import print_top_bar
from .compositions.verticalbar import print_vertical_bar


class PlayEffect(Print):
    """The Game's Play Screen"""

    def __init__(self, screen, game_state):
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )
        self.play_y = self.screen.height - 4
        self.current = ("Dungeon Depths", 0)
        self.game = game_state

    def process_event(self, event):
        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None
            if event.key_code == ord("b") or event.key_code == ord("B"):
                self.game.current_scene = "Start"
                raise NextScene("Start")
            # These effects are palceholder.
            if event.key_code == ord("1"):
                self.current = ("Character 1", 1)
            if event.key_code == ord("2"):
                self.current = ("Character 2", 2)
            if event.key_code == ord("3"):
                self.current = ("Character 3", 3)
            if event.key_code == ord("4"):
                self.current = ("Character 4", 4)
            if event.key_code == ord("5"):
                self.current = ("Character 5", 5)
            if event.key_code == ord("6"):
                self.current = ("Character 6", 6)
            if event.key_code == ord("7"):
                self.current = ("Character 7", 7)
            if event.key_code == ord("8"):
                self.current = ("Character 8", 8)
        return event

    def _update(self, frame_no):
        print_top_bar(self, self.current[0])
        print_vertical_bar(self, self.screen.width // 5)

        horizontal_sep = "=" * ((self.screen.width // 5) - 1)
        for i in range(1, 9):
            line = (self.play_y * i // 8) + 4
            line_above = (self.play_y * i // 8) - (self.play_y // 8) + 4
            self.screen.print_at(horizontal_sep, 1, line, 7, 1)
            if i == self.current[1]:
                polygon = [
                    (1, line_above),
                    (
                        (self.screen.width // 5),
                        line_above,
                    ),
                    ((self.screen.width // 5), line),
                    (1, line),
                ]
                self.screen.fill_polygon([polygon], 3, 0)
            self.screen.paint(
                text=f"[{i}]",
                x=3,
                y=line_above + 1,
                colour_map=[(1, 1, 0), (3, 4, 0), (1, 1, 0)],
            )
            if i > self.game.slots:
                self.screen.print_at(
                    "Purchase Slot for 200 Silver",  # Placeholder
                    x=7,
                    y=line_above + 1,
                )
            else:
                self.screen.print_at(
                    f"{self.game.characters[i - 1].name}",
                    x=7,
                    y=line_above + 1,
                )
