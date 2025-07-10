from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.widgets import Frame, Layout, Text, RadioButtons, Button, TextBox
from asciimatics.screen import Screen

from src.const import MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH, PALETTE

from src.scenes.compositions.topbar import print_top_bar
from src.scenes.compositions.verticalbar import print_vertical_bar
from src.scenes.compositions.screensize import print_screen_size

from src.actors.characters.classes.classes import Classes, ClassesDescriptions
from src.actors.characters.character import Character


class CharacterCreationView(Frame):
    def __init__(self, screen, game_state, slot):
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

        layout = Layout([1, 1], fill_frame=True)
        self.add_layout(layout)

        # Creates a text input field.
        self.name_text = Text("Name:", "name")
        layout.add_widget(self.name_text, 0)

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
            10,
            name="class_info",
            as_string=True,
            line_wrap=True,
            readonly=True,
            tab_stop=False,
        )
        self.class_info.hide_cursor = True
        self.class_info.value = self._set_info()
        layout.add_widget(self.class_info, 1)

        # Buttons for 'Ok' and 'Cancel'
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("[O]K", self._ok), 0)
        layout2.add_widget(Button("[C]ancel", self._cancel), 3)

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
        self.game.characters[self.slot - 1] = Character(selected_class, character_name)
        raise NextScene("Play")

    def _cancel(self):
        self.game.current_sub = ("Default", 0)
        raise NextScene("Play")

    def process_event(self, event):
        if self.name_text._has_focus:
            return super().process_event(event)

        if hasattr(event, "key_code"):
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.

            # Select Radio Button options from 1 to 8
            if ord("1") <= event.key_code <= ord("9"):
                class_index = event.key_code - ord("1")
                if class_index < len(self.classes_radio._options):
                    self.classes_radio.value = self.classes_radio._options[class_index][
                        1
                    ]
                    return None
            if event.key_code == ord("o") or event.key_code == ord("O"):
                self._ok()
                return None
            if event.key_code == ord("c") or event.key_code == ord("C"):
                self._cancel()
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

    def __init__(self, screen, game_state):

        # This is only used for initialization and isn't displayed during normal operations.
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )
        self.play_y = self.screen.height - 4
        self.current = ("Dungeon Depths", 0)
        self.game = game_state
        self._char_creation_active = False

    def process_event(self, event):
        if self._char_creation_active:
            return event

        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None  # Disables global exit from this screen.
            if event.key_code == ord("b") or event.key_code == ord("B"):
                self.game.current_scene = "Start"
                raise NextScene("Start")
            # These effects are palceholder.
            if event.key_code == ord("1"):
                self.activate_character_creator(1)
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
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
            print_screen_size(self)
        else:
            print_top_bar(self, self.current[0])
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
                    self.screen.print_at(
                        text=f"{self.game.characters[i - 1].name}",
                        x=7,
                        y=line_above + 1,
                    )

            # Placholder for the CharacterCreationView logic.
            match self.game.current_sub[0]:
                case "char_creation":
                    if not self._char_creation_active:
                        self.scene.add_effect(
                            CharacterCreationView(
                                self.screen, self.game, self.game.current_sub[1]
                            )
                        )
                        self._char_creation_active = True
                case _:
                    self._char_creation_active = False
                    self.screen.print_at(
                        "Default",
                        50,
                        (self.screen.height // 2) + 4,
                        Screen.COLOUR_WHITE,
                        1,
                    )

    def activate_character_creator(self, slot):
        if (
            self.game.characters[slot - 1].actor_type == "None"
            and self.game.slots >= slot
        ):
            self.game.current_sub = ("char_creation", slot)
