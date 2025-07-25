from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.widgets import (
    Frame,
    Layout,
    Text,
    RadioButtons,
    Button,
    TextBox,
    Divider,
    PopUpDialog,
)
from asciimatics.screen import Screen

from src.const import (
    MIN_SCREEN_HEIGHT,
    MIN_SCREEN_WIDTH,
    PALETTE,
    MAX_CHARACTER_SLOT,
    START_SCENE,
)
from src.game import GameState
from src.save import write_save

from src.game import SubScreen

from src.scenes.compositions.topbar import print_top_bar
from src.scenes.compositions.verticalbar import print_vertical_bar
from src.scenes.compositions.screensize import print_screen_size

from src.game_types import ActorType
from src.actors.characters.classes.classes import Classes, ClassesDescriptions
from src.actors.characters.character import Character


class QuitPopup(PopUpDialog):
    def __init__(self, screen, game_state: GameState):
        self.game = game_state
        super().__init__(
            screen,
            "Save and Quit to Main Menu?",
            ["OK", "Cancel"],
            on_close=self._on_exit,
            has_shadow=True,
        )
        self.palette = PALETTE

    def _on_exit(self, choice):
        if choice == 0:
            self._ok()
        else:
            self._cancel()

    def _ok(self):
        if not self.game.is_empty_save:
            write_save(self.game)
        self.screen.clear_buffer(0, 0, 0)
        self.scene.reset()
        self.game.set_scene(START_SCENE)
        raise NextScene(START_SCENE)

    def _cancel(self):
        self.screen.clear_buffer(0, 0, 0)


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
        self.character_header = TextBox(
            1,
            name="character_header",
            as_string=True,
            line_wrap=False,
            readonly=True,
            tab_stop=False,
        )
        self.character_header.hide_cursor = True
        self.character_header.value = "Manage Character"
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
        self.dungeon_header = TextBox(
            1,
            name="dungeon_header",
            as_string=True,
            line_wrap=False,
            readonly=True,
            tab_stop=False,
        )
        self.dungeon_header.hide_cursor = True
        self.dungeon_header.value = "Dungeons"
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
        self.training_header = TextBox(
            1,
            name="training_header",
            as_string=True,
            line_wrap=False,
            readonly=True,
            tab_stop=False,
        )
        self.training_header.hide_cursor = True
        self.training_header.value = "Training"
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
        self.options_header = TextBox(
            1,
            name="options_header",
            as_string=True,
            line_wrap=False,
            readonly=True,
            tab_stop=False,
        )
        self.options_header.hide_cursor = True
        self.options_header.value = "Options"
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
        pass

    def _dungeon(self):
        pass

    def _combat(self):
        pass

    def _craft(self):
        pass

    def _secondary(self):
        pass

    def _guide(self):
        self.parent.activate_guide()

    def _save(self):
        pass

    def _back(self):
        self.parent.activate_quit_confirm()

    def process_event(self, event):
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
                    self.button_back.blur()
                    self.button_character_sheet.focus()

            if event.key_code in (ord("e"), ord("E")):
                if self.button_equip_menu._has_focus:
                    self._equip()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_equip_menu.focus()

            if event.key_code in (ord("v"), ord("V")):
                if self.button_inventory._has_focus:
                    self._inventory()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_inventory.focus()

            if event.key_code in (ord("i"), ord("I")):
                if self.button_dismiss._has_focus:
                    self._dismiss()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_dismiss.focus()

            if event.key_code in (ord("p"), ord("P")):
                if self.button_party_menu._has_focus:
                    self._party()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_party_menu.focus()

            if event.key_code in (ord("d"), ord("D")):
                if self.button_dungeon_menu._has_focus:
                    self._dungeon()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_dungeon_menu.focus()

            if event.key_code in (ord("t"), ord("T")):
                if self.button_combat_train._has_focus:
                    self._combat()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_combat_train.focus()

            if event.key_code in (ord("r"), ord("R")):
                if self.button_crafting_train._has_focus:
                    self._craft()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_crafting_train.focus()

            if event.key_code in (ord("k"), ord("K")):
                if self.button_secondary_train._has_focus:
                    self._secondary()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_secondary_train.focus()

            if event.key_code in (ord("g"), ord("G")):
                if self.button_guide._has_focus:
                    self._guide()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
                    self.button_guide.focus()

            if event.key_code in (ord("s"), ord("S")):
                if self.button_save._has_focus:
                    self._save()
                else:
                    for a in self.activities:
                        a.blur()
                    self.button_back.blur()
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

        return event


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
                self.parent.activate_quit_confirm()
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character(slot)
        return event


class CharacterCreationView(Frame):
    def __init__(self, screen, game_state: GameState, slot, parent):
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
            is_modal=True,
        )
        self.palette = PALETTE
        self.game = game_state
        self.slot = slot
        self.parent = parent

        layout = Layout([1, 1], fill_frame=True, gutter=1)
        self.add_layout(layout)

        # Creates a text input field.
        self.name_text = Text("Name:", "name")
        layout.add_widget(self.name_text, 0)

        layout.add_widget(Divider(draw_line=False), 0)

        # Creates a list of available classes
        classes_options = []
        for i, c in enumerate(Classes):
            classes_options.append((f"{i + 1}. {c.value.capitalize()}", c))
        self.classes_radio = RadioButtons(
            classes_options,
            label="Class:",
            name="character_class",
            on_change=self._on_change,
        )
        layout.add_widget(self.classes_radio, 0)

        # Shows details about the selected class to the user.
        self.class_info = TextBox(
            20,
            name="class_info",
            as_string=True,
            line_wrap=True,
            readonly=True,
            tab_stop=False,
        )
        self.class_info.hide_cursor = True
        self.class_info.value = self._set_info()
        layout.add_widget(self.class_info, 1)

        # Shows additional details about character creation.
        self.add_info = TextBox(
            15,
            name="additional_info",
            as_string=True,
            line_wrap=False,
            readonly=True,
            tab_stop=False,
        )
        self.add_info.hide_cursor = True
        self.add_info.value = """
\n-The character's ancestry will be chosen at random.
\n-The character will be given 4 abilities at random\nfrom their class pool.
\n-The character's health, attributes, and skills\nwill be calculated based on their class and their\nancestry.
\n-The character will be given a set of equipment\nfit for their class.
"""
        layout.add_widget(self.add_info, 0)

        # Buttons for 'Ok' and 'Cancel'
        layout2 = Layout([1, 1, 1, 1])
        self.button_ok = Button("[O]K", self._ok)
        self.button_cancel = Button("[C]ancel", self._cancel)
        self.add_layout(layout2)
        layout2.add_widget(self.button_ok, 0)
        layout2.add_widget(self.button_cancel, 3)

        # The layout becomes fixed and the position of all widgets is calculated.
        self.fix()

    def _on_change(self):
        self.save()
        self.class_info.value = self._set_info()

    def _ok(self):
        self.save()
        character_name = self.data.get("name")
        if not character_name:
            character_name = "Nameless"
        selected_class = self.data.get("character_class")
        if not selected_class:
            selected_class = Classes.MARAUDER
        self.game.set_character(
            Character(selected_class, character_name), self.slot - 1
        )
        self.game.debug_log(self.game.get_character(self.slot - 1).to_json())
        if self.game.is_empty_save:
            self.game.is_empty_save = False
        self.scene.remove_effect(self)
        self.screen.clear_buffer(0, 0, 0)
        self.parent.activate_character(self.slot)

    def _cancel(self):
        self.scene.remove_effect(self)
        self.screen.clear_buffer(0, 0, 0)
        self.parent.activate_guide()

    def process_event(self, event):
        if hasattr(event, "key_code"):

            if self.name_text._has_focus:
                if event.key_code in (ord("\n"), ord("\r")):
                    self.name_text.blur()
                    self.classes_radio.focus()
                    return None
                return super().process_event(event)

            if self.classes_radio._has_focus:
                # Select Radio Button options from 1 to 8
                if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                    class_index = event.key_code - ord("1")
                    if class_index < len(self.classes_radio._options):
                        self.classes_radio.value = self.classes_radio._options[
                            class_index
                        ][1]
                        return None
                if event.key_code in (ord("\n"), ord("\r")):
                    self.classes_radio.blur()
                    self.button_ok.focus()
                    return None
                if event.key_code in (ord("o"), ord("O")):
                    self.classes_radio.blur()
                    self.button_ok.focus()
                    return None
                if event.key_code in (ord("c"), ord("C")):
                    self.classes_radio.blur()
                    self.button_cancel.focus()
                    return None

            if self.button_ok._has_focus:
                if event.key_code in (ord("\n"), ord("\r")):
                    self._ok()
                    return None
                if event.key_code in (ord("o"), ord("O")):
                    self._ok()
                    return None
                if event.key_code in (ord("c"), ord("C")):
                    self.button_ok.blur()
                    self.button_cancel.focus()
                    return None

            if self.button_cancel._has_focus:
                if event.key_code in (ord("\n"), ord("\r")):
                    self._cancel()
                    return None
                if event.key_code in (ord("o"), ord("O")):
                    self.button_cancel.blur()
                    self.button_ok.focus()
                    return None
                if event.key_code in (ord("c"), ord("C")):
                    self._cancel()
                    return None

            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
        return super().process_event(event)

    def _set_info(self):
        match self.classes_radio.value:
            case Classes.MARAUDER:
                return ClassesDescriptions.DESC_MARAUDER.value
            case Classes.STALKER:
                return ClassesDescriptions.DESC_STALKER.value
            case Classes.OCCULTIST:
                return ClassesDescriptions.DESC_OCCULTIST.value
            case Classes.PENITENT:
                return ClassesDescriptions.DESC_PENITENT.value
            case Classes.PRIMALIST:
                return ClassesDescriptions.DESC_PRIMALIST.value
            case Classes.SENTINEL:
                return ClassesDescriptions.DESC_SENTINEL.value
            case Classes.TEMPLAR:
                return ClassesDescriptions.DESC_TEMPLAR.value
            case Classes.CENOBITE:
                return ClassesDescriptions.DESC_CENOBITE.value
            case _:
                return "Something went wrong finding the class description!"


class PlayEffect(Print):
    """The Game's Play Screen"""

    def __init__(self, screen, game_state: GameState):

        # This is only used for initialization and isn't displayed during normal operations.
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )
        self.play_y = self.screen.height - 4
        self.current_header = "Dungeon Depths"
        self.game = game_state

    def process_event(self, event):
        if self.game.get_sub_screen() in (
            SubScreen.CHAR_CREATION,
            SubScreen.GUIDE,
            SubScreen.ACTIVITY_MENU,
        ):
            return event

        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("b"), ord("B")):
                self.activate_quit_confirm()
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.activate_character(slot)
            if event.key_code in (ord("g"), ord("G")):
                self.activate_guide()
        return event

    def _update(self, frame_no):
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
            print_screen_size(self)
        else:
            print_top_bar(self, self.current_header)
            print_vertical_bar(self, self.screen.width // 5, self.screen.height)

            horizontal_sep = "=" * ((self.screen.width // 5) - 1)
            for i in range(1, 9):
                # Try to split the character into eights.
                # We keep track of the line above to avoid rewriting the formula when drawing polygons.
                line = (self.play_y * i // 8) + 4
                line_above = (self.play_y * i // 8) - (self.play_y // 8) + 4
                self.screen.print_at(
                    text=horizontal_sep,
                    x=1,
                    y=line,
                    colour=Screen.COLOUR_WHITE,
                    attr=Screen.A_BOLD,
                )

                # Draws the polygon highlighting the currently selected character slot.
                # The polygon is 4 points in tuples (x, y).
                if i == self.game.get_sub_data():
                    polygon = [
                        (1, line_above),
                        (
                            (self.screen.width // 5),
                            line_above,
                        ),
                        ((self.screen.width // 5), line),
                        (1, line),
                    ]
                    self.screen.fill_polygon(
                        [polygon], Screen.COLOUR_YELLOW, Screen.COLOUR_BLACK
                    )

                # Writes the selection number for each character slot.
                self.screen.paint(
                    text=f"[{i}]",
                    x=3,
                    y=line_above + 1,
                    colour_map=[
                        (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                        (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                        (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                    ],
                )

                # Writes a buy offer if the slot is above the current maximum slot.
                # Otherwise, writes the character's name.
                if i > self.game.get_slots():
                    self.screen.print_at(
                        text="Purchase: 200 Silver",  # Placeholder
                        x=7,
                        y=line_above + 1,
                    )
                else:
                    chara = self.game.get_character(i - 1)
                    self.screen.print_at(
                        text=f"{chara.get_name()}",
                        x=7,
                        y=line_above + 1,
                    )
                    if chara.get_actor_type() == ActorType.CHARACTER:
                        self.screen.print_at(
                            text=f"{chara.get_char_class().name}",  # Add the character's current activity later.
                            x=7,
                            y=line_above + 2,
                        )

    def reset(self):
        super().reset()
        sub, data = self.game.get_sub()
        match sub:
            case SubScreen.DEFAULT | SubScreen.GUIDE:
                self.activate_guide()
            case SubScreen.CHAR_CREATION | SubScreen.ACTIVITY_MENU:
                self.activate_character(data)
            # Other Cases will go here.

    def activate_character(self, slot):
        chara = self.game.get_character(slot - 1)
        self.current_header = f"{slot}—{chara.get_name()}"
        if chara.get_actor_type() == ActorType.NONE and self.game.get_slots() >= slot:
            self.game.info_log("Activating Character Creator...")
            self.game.set_sub((SubScreen.CHAR_CREATION, slot))
            self.scene.add_effect(
                CharacterCreationView(
                    self.screen, self.game, self.game.get_sub_data(), self
                )
            )
        elif (
            chara.get_actor_type() == ActorType.CHARACTER
            and self.game.get_slots() >= slot
        ):
            self.game.set_sub((SubScreen.ACTIVITY_MENU, slot))
            self.scene.add_effect(ActivityMenu(self.screen, self.game, self))

    def activate_quit_confirm(self):
        self.scene.add_effect(QuitPopup(self.screen, self.game))

    def activate_guide(self):
        self.game.info_log("Activating Guide...")
        self.game.set_sub_screen(SubScreen.GUIDE)
        self.current_header = "Guide"
        self.scene.add_effect(GuideView(self.screen, self.game, self))
