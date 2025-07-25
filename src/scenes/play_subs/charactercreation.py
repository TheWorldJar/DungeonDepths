from asciimatics.widgets import (
    Frame,
    Layout,
    Text,
    RadioButtons,
    Button,
    TextBox,
    Divider,
)

from src.const import (
    PALETTE,
    MAX_CHARACTER_SLOT,
)
from src.game import GameState

from src.actors.characters.character import Character
from src.actors.characters.classes.classes import Classes, ClassesDescriptions


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
