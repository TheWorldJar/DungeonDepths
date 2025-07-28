from asciimatics.widgets import (
    Frame,
    Layout,
    Button,
    Label,
    Divider,
)

from src.const import (
    PALETTE,
    MAX_CHARACTER_SLOT,
)
from src.game import GameState


class ActivityMenu(Frame):
    def __init__(self, screen, game_state: GameState, parent):
        super().__init__(
            screen,
            screen.height - 4,
            screen.width * 4 // 5,
            x=screen.width // 5 + 1,
            y=4,
            hover_focus=True,
            title="Activity Menu",
            reduce_cpu=True,
            has_border=False,
            is_modal=True,
        )
        self.palette = PALETTE
        self.game = game_state
        self.parent = parent

        layout_top = Layout([1, 1], fill_frame=True, gutter=1)
        self.add_layout(layout_top)

        self.activities = []

        # Manage Character
        self.character_header = Label("Manage Character", 1, "^")
        self.character_header.custom_colour = "title"
        self.button_character_sheet = Button("[C]haracter Sheet", self._sheet)
        self.button_equip_menu = Button("[E]quip", self._equip)
        self.button_inventory = Button("[V]iew Inventory", self._inventory)
        self.button_dismiss = Button("D[i]smiss Character", self._dismiss)
        self.activities.extend(
            [
                self.character_header,
                Divider(draw_line=True, height=1),
                self.button_character_sheet,
                self.button_equip_menu,
                self.button_inventory,
                self.button_dismiss,
                Divider(draw_line=False, height=1),
            ]
        )

        # Dungeons
        self.dungeon_header = Label("Dungeons", 1, "^")
        self.dungeon_header.custom_colour = "title"
        self.button_party_menu = Button("[P]arty Sheet", self._party)
        self.button_dungeon_menu = Button("[D]ungeons", self._dungeon)
        self.activities.extend(
            [
                self.dungeon_header,
                Divider(draw_line=True, height=1),
                self.button_party_menu,
                self.button_dungeon_menu,
                Divider(draw_line=False, height=1),
            ]
        )

        # Training
        self.training_header = Label("Training", 1, "^")
        self.training_header.custom_colour = "title"
        self.button_combat_train = Button("Combat [T]raining", self._combat)
        self.button_crafting_train = Button("C[r]afting", self._craft)
        self.button_secondary_train = Button("Secondary S[k]ills", self._secondary)
        self.activities.extend(
            [
                self.training_header,
                Divider(draw_line=True, height=1),
                self.button_combat_train,
                self.button_crafting_train,
                self.button_secondary_train,
                Divider(draw_line=False, height=1),
            ]
        )

        # Options
        self.options_header = Label("Options", 1, "^")
        self.options_header.custom_colour = "title"
        self.button_guide = Button("[G]uide", self._guide)
        self.button_save = Button("[S]ave", self._save)
        self.activities.extend(
            [
                self.options_header,
                Divider(draw_line=True, height=1),
                self.button_guide,
                self.button_save,
                Divider(draw_line=False, height=1),
            ]
        )

        for a in self.activities:
            layout_top.add_widget(a)

        layout_bottom = Layout([1])
        self.add_layout(layout_bottom)

        self.button_back = Button("[B]ack to Main Menu", self._back)
        layout_bottom.add_widget(self.button_back)

        self.activities.append(self.button_back)

        self.fix()

    # To be implemented
    def _sheet(self):
        pass

    def _equip(self):
        pass

    def _inventory(self):
        pass

    def _dismiss(self):
        pass

    def _party(self):
        self.scene.remove_effect(self)
        self.parent.activate_party_menu()

    def _dungeon(self):
        pass

    def _combat(self):
        pass

    def _craft(self):
        pass

    def _secondary(self):
        pass

    def _guide(self):
        self.scene.remove_effect(self)
        self.parent.activate_guide()

    def _save(self):
        pass

    def _back(self):
        self.parent.activate_quit_confirm()

    def process_event(self, event):
        if hasattr(event, "x") or hasattr(event, "y"):
            return None  # Disables global mouse events
        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.

            if event.key_code in (ord("c"), ord("C")):
                if self.button_character_sheet._has_focus:
                    self._sheet()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_character_sheet.focus()

            if event.key_code in (ord("e"), ord("E")):
                if self.button_equip_menu._has_focus:
                    self._equip()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_equip_menu.focus()

            if event.key_code in (ord("v"), ord("V")):
                if self.button_inventory._has_focus:
                    self._inventory()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_inventory.focus()

            if event.key_code in (ord("i"), ord("I")):
                if self.button_dismiss._has_focus:
                    self._dismiss()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_dismiss.focus()

            if event.key_code in (ord("p"), ord("P")):
                if self.button_party_menu._has_focus:
                    self._party()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_party_menu.focus()

            if event.key_code in (ord("d"), ord("D")):
                if self.button_dungeon_menu._has_focus:
                    self._dungeon()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_dungeon_menu.focus()

            if event.key_code in (ord("t"), ord("T")):
                if self.button_combat_train._has_focus:
                    self._combat()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_combat_train.focus()

            if event.key_code in (ord("r"), ord("R")):
                if self.button_crafting_train._has_focus:
                    self._craft()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_crafting_train.focus()

            if event.key_code in (ord("k"), ord("K")):
                if self.button_secondary_train._has_focus:
                    self._secondary()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_secondary_train.focus()

            if event.key_code in (ord("g"), ord("G")):
                if self.button_guide._has_focus:
                    self._guide()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_guide.focus()

            if event.key_code in (ord("s"), ord("S")):
                if self.button_save._has_focus:
                    self._save()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_save.focus()

            if event.key_code in (ord("b"), ord("B")):
                if self.button_back._has_focus:
                    self._back()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.focus()

            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character(slot)

            if event.key_code in (ord("\n"), ord("\r")):
                for a in self.activities:
                    if a._has_focus:
                        a._on_click()
                return None  # Disables global scene cycling.
        return super().process_event(event)
