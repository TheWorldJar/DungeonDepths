from asciimatics.widgets import (
    Frame,
    Layout,
    Label,
    Divider,
    Button,
    PopupMenu,
    PopUpDialog,
)

from src.const import PALETTE, MAX_CHARACTER_SLOT
from src.game import GameState, SubScreen
from src.game_types import ActorType


class SwitchMenu(PopupMenu):
    def __init__(self, screen, game_state: GameState, slot1: int):
        self.game = game_state
        self.slot1 = slot1
        menu_items = []
        for i, c in enumerate(self.game.get_all_characters()):
            if c.get_actor_type() == ActorType.CHARACTER and i != self.slot1:
                menu_items.append((c.get_name(), lambda x=i: self._switch(x)))
        menu_items.append(("CANCEL", self._cancel))

        super().__init__(
            screen,
            menu_items=menu_items,
            x=screen.width // 2,
            y=screen.height // 2,
        )

        self.palette = PALETTE

    def _switch(self, slot2: int):
        self.game.swap_characters(self.slot1, slot2)
        self.screen.clear_buffer(0, 0, 0)
        self.scene.reset()

    def _cancel(self):
        self.screen.clear_buffer(0, 0, 0)


class BadSwitchPopup(PopUpDialog):
    def __init__(self, screen):
        super().__init__(
            screen,
            "No valid character to switch with!",
            ["OK"],
            on_close=self._on_exit,
            has_shadow=True,
        )
        self.palette = PALETTE

    def _on_exit(self, choice):
        self.screen.clear_buffer(0, 0, 0)
        self.scene.reset()


class PartyMenu(Frame):
    activities: list[Label | Button | Divider]

    def __init__(self, screen, game_state: GameState, parent):
        super().__init__(
            screen,
            screen.height - 4,
            screen.width * 4 // 5,
            x=screen.width // 5 + 1,
            y=4,
            hover_focus=True,
            title="Party Menu",
            reduce_cpu=True,
            has_border=False,
            is_modal=True,
        )
        self.palette = PALETTE
        self.game = game_state
        self.parent = parent

        layout_top = Layout([1, 1], fill_frame=True, gutter=1)
        self.add_layout(layout_top)

        self.party_instructions = Label("Select a Character to swap them")
        self.party_instructions.custom_colour = "edit_text"

        self.party_header = Label("Current Party")
        self.party_header.custom_colour = "title"

        self.activities = [
            self.party_instructions,
            Divider(draw_line=False, height=1),
            self.party_header,
            Divider(draw_line=True, height=1),
        ]

        for i, c in enumerate(self.game.get_party()):
            self.game.debug_log(f"Party[{i}]: Actor Type: {c.get_actor_type()}")
            if c.get_actor_type() == ActorType.CHARACTER:
                self.activities.append(
                    Button(
                        c.get_name(),
                        lambda x=i: self._on_switch(x),
                        add_box=False,
                    )
                )

        self.not_party_header = Label("Other Characters")
        self.not_party_header.custom_colour = "title"

        self.activities.extend(
            [
                Divider(draw_line=False, height=1),
                self.not_party_header,
                Divider(draw_line=True, height=1),
            ]
        )

        for j, n in enumerate(self.game.get_not_party()):
            self.game.debug_log(f"Party[{j + 4}]: Actor Type: {n.get_actor_type()}")
            if n.get_actor_type() == ActorType.CHARACTER:
                self.activities.append(
                    Button(
                        n.get_name(),
                        lambda x=j: self._on_switch(x + 4),
                        add_box=False,
                    )
                )

        self.game.debug_log(f"{len(self.activities)} Activities")
        for a in self.activities:
            self.game.debug_log(f"Activities: {a}")
            layout_top.add_widget(a)

        # TODO: Implement party information in the second column of layout_top.

        layout_bottom = Layout([1])
        self.add_layout(layout_bottom)

        self.button_back = Button("[B]ack to Activity Menu", self._back)
        layout_bottom.add_widget(self.button_back)

        self.activities.append(self.button_back)

        self.fix()

    def _on_switch(self, slot1: int):
        if self.game.get_party_member(1).get_actor_type() != ActorType.CHARACTER:
            self.scene.add_effect(BadSwitchPopup(self.screen))
        else:
            self.scene.add_effect(SwitchMenu(self.screen, self.game, slot1))

    def _back(self):
        self.screen.clear_buffer(0, 0, 0)
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

            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character(slot)

            if event.key_code in (ord("\n"), ord("\r")):
                for a in self.activities:
                    if a._has_focus:
                        a._on_click()
                return None  # Disables global scene cycling.

            if event.key_code in (ord("b"), ord("B")):
                if self.button_back._has_focus:
                    self._back()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.focus()
        return super().process_event(event)
