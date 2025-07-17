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

from src.actors.actor import ActorType
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
            if event.key_code in (ord("b"), ("B")):
                self.parent.activate_quit_confirm()
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.scene.remove_effect(self)
                self.parent.activate_character_creator(slot)
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
\n-The character will be given a set of equipement\nfit for their class.
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
        self.parent.activate_guide()

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
        if self.game.get_sub_screen() in (SubScreen.CHAR_CREATION, SubScreen.GUIDE):
            return event

        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("b"), ("B")):
                self.activate_quit_confirm()
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if ord("1") <= event.key_code <= ord(str(MAX_CHARACTER_SLOT)):
                slot = event.key_code - ord("0")
                self.activate_character_creator(slot)
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
                if i == self.current_header[1]:
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
                if i > self.game.slots:
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
                    if chara.actor_type == ActorType.CHARACTER:
                        self.screen.print_at(
                            text=f"{chara.get_char_class().value.upper()}",  # Add the character's current activity later.
                            x=7,
                            y=line_above + 2,
                        )

    def reset(self):
        super().reset()
        sub, data = self.game.get_sub()
        match sub:
            case SubScreen.DEFAULT | SubScreen.GUIDE:
                self.activate_guide()
            case SubScreen.CHAR_CREATION:
                self.activate_character_creator(data)
            # Other Cases will go here.

    def activate_character_creator(self, slot):
        chara = self.game.get_character(slot - 1)
        self.current_header = f"{slot}—{chara.name}"
        if chara.actor_type == ActorType.NONE and self.game.slots >= slot:
            self.game.info_log("Activating Character Creator...")
            self.game.set_sub((SubScreen.CHAR_CREATION, slot))
            self.scene.add_effect(
                CharacterCreationView(
                    self.screen, self.game, self.game.get_sub_data(), self
                )
            )

    def activate_quit_confirm(self):
        self.scene.add_effect(QuitPopup(self.screen, self.game))

    def activate_guide(self):
        self.game.info_log("Activating Guide...")
        self.game.set_sub((SubScreen.GUIDE, 0))
        self.current_header = "Guide"
        self.scene.add_effect(GuideView(self.screen, self.game, self))
