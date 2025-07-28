from asciimatics.widgets import (
    Frame,
    Layout,
    Label,
    Button,
)

from src.const import (
    PALETTE,
    MAX_CHARACTER_SLOT,
)
from src.game import GameState, SubScreen


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

        layout_top = Layout([1], fill_frame=True)
        self.add_layout(layout_top)

        self.guide_info = Label(
            """
- Choose a character slot using a number key [1–8].
- If you haven't recruited a character in that slot, you will be brought to the character creator.
- Otherwise, you will select that character to give them orders.
    
- In other screens, actions will be chosen with the key in between brackets: [Key]
    
- To go back to the Main Menu, press [B].
""",
            screen.height - 4,
        )
        self.guide_info.custom_colour = "edit_text"
        layout_top.add_widget(self.guide_info, 0)

        layout_bottom = Layout([1])
        self.add_layout(layout_bottom)

        if self.game.get_sub_data() == 0:
            back_text = "[B]ack to the Main Menu"
        else:
            back_text = "[B]ack to Activity Menu"
        self.button_back = Button(back_text, self._back)
        layout_bottom.add_widget(self.button_back)

        self.fix()

    def _back(self):
        self.screen.clear_buffer(0, 0, 0)
        if self.game.get_sub_data() == 0:
            self.parent.activate_quit_confirm()
        else:
            self.game.set_sub_screen(SubScreen.ACTIVITY_MENU)
            self.scene.remove_effect(self)
            self.scene.reset()

    def process_event(self, event):
        if hasattr(event, "x") or hasattr(event, "y"):
            return None  # Disables global mouse events
        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("b"), ord("B")):
                self._back()
            if event.key_code in (ord("\n"), ord("\r")):
                if self.button_back._has_focus():
                    self._back()
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character(slot)
        return super().process_event(event)
