from asciimatics.widgets import (
    Frame,
    Layout,
    TextBox,
)

from src.const import (
    PALETTE,
    MAX_CHARACTER_SLOT,
)
from src.game import GameState


class GuideView(Frame):
    def __init__(self, screen, game_state: GameState, parent):
        super().__init__(
            screen,
            screen.height - 4,  # The top bar occupies the first 4 lines.
            screen.width * 4 // 5,  # The Character menu occupies the left fifth.
            x=screen.width // 5 + 1,
            y=4,
            hover_focus=True,
            title="Character Creation",
            reduce_cpu=True,
            has_border=False,
            is_modal=False,
        )
        self.palette = PALETTE
        self.game = game_state
        self.parent = parent

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        self.guide_info = TextBox(
            self.screen.height - 2,
            name="guide_info",
            as_string=True,
            line_wrap=True,
            readonly=True,
            tab_stop=False,
        )
        self.guide_info.hide_cursor = True

        # Placeholder
        self.guide_info.value = """
GUIDE
- Choose a character slot using a number key [1–8].
    - If you haven't recruited a character in that slot, you will be brought to the character creator.
    - Otherwise, you will select that character to give them orders.

- In other screens, actions will be chosen with the key in between brackets: [Key]

- To go back to the Main Menu, press [B].
"""
        layout.add_widget(self.guide_info, 0)

        self.fix()

    def process_event(self, event):
        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("b"), ord("B")):
                if self.game.get_sub_data() == 0:
                    self.parent.activate_quit_confirm()
                else:
                    self.scene.remove_effect(self)
                    self.parent.activate_character(self.game.get_sub_data())
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character(slot)
        return super().process_event(event)
