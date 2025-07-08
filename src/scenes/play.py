from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.widgets import Frame, Layout, Text, ListBox, Button, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from .compositions.topbar import print_top_bar
from .compositions.verticalbar import print_vertical_bar
from .compositions.screensize import print_screen_size, MIN_WIDTH, MIN_HEIGHT
from src.actors.characters.classes.classes import Classes
from src.actors.characters.character import Character


class CharacterCreationView(Frame):
    def __init__(self, screen, game_state, slot):
        super().__init__(
            screen,
            screen.height - 4,
            screen.width * 4 // 5,
            x=screen.width // 5 + 1,
            y=4,
            hover_focus=True,
            title="Character Creation",
            reduce_cpu=True,
            has_border=False,
            is_modal=True,
        )
        self.palette = {
            "background": (7, 2, 0),
            "shadow": (7, 2, 0),
            "disabled": (7, 2, 0),
            "invalid": (7, 2, 0),
            "label": (7, 2, 0),
            "borders": (7, 2, 0),
            "scroll": (7, 2, 0),
            "title": (7, 2, 0),
            "edit_text": (7, 2, 0),
            "button": (7, 2, 0),
            "control": (7, 2, 0),
            "field": (7, 2, 0),
            "focus_button": (7, 2, 0),
            "focus_control": (7, 2, 0),
            "focus_field": (7, 2, 0),
            "focus_edit_text": (7, 2, 0),
            "focus_label": (7, 2, 0),
            "selected_field": (7, 2, 0),
            "selected_control": (7, 2, 0),
            "selected_button": (7, 2, 0),
            "selected_focus_field": (7, 2, 0),
            "selected_focus_control": (7, 2, 0),
            "selected_focus_button": (7, 2, 0),
        }
        self.game = game_state
        self.slot = slot

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Text("Name:", "name", on_change=self._on_change))

        classes_options = [(c.value.capitalize(), c) for c in Classes]
        layout.add_widget(
            ListBox(
                Widget.FILL_FRAME,
                classes_options,
                name="character_class",
                on_change=self._on_change,
                add_scroll_bar=True,
            )
        )

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)

        self.fix()

    def _on_change(self):
        # Placeholder for dynamic updates if needed
        pass

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
        self._char_creation_active = False

    def process_event(self, event):
        if self._char_creation_active:
            return event

        if hasattr(event, "key_code"):
            self.screen.clear_buffer(0, 0, 0)
            if event.key_code == ord("q") or event.key_code == ord("Q"):
                return None
            if event.key_code == ord("b") or event.key_code == ord("B"):
                self.game.current_scene = "Start"
                raise NextScene("Start")
            # These effects are palceholder.
            if event.key_code == ord("1"):
                self.character_creator(1)
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
        if self.screen.width < MIN_WIDTH or self.screen.height < MIN_HEIGHT:
            print_screen_size(self)
        else:
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
                        "Purchase: 200 Silver",  # Placeholder
                        x=7,
                        y=line_above + 1,
                    )
                else:
                    self.screen.print_at(
                        f"{self.game.characters[i - 1].name}",
                        x=7,
                        y=line_above + 1,
                    )
            # Placholder
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
                        7,
                        1,
                    )

    def character_creator(self, slot):
        if (
            self.game.characters[slot - 1].actor_type == "None"
            and self.game.slots >= slot
        ):
            self.game.current_sub = ("char_creation", slot)
