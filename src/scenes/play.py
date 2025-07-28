from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.widgets import (
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
from src.game_types import ActorType
from src.game import GameState, SubScreen
from src.save import write_save

from src.scenes.compositions.topbar import print_top_bar
from src.scenes.compositions.verticalbar import print_vertical_bar
from src.scenes.compositions.screensize import print_screen_size

from src.scenes.play_subs.charactercreation import CharacterCreationView
from src.scenes.play_subs.guide import GuideView
from src.scenes.play_subs.activitymenu import ActivityMenu
from src.scenes.play_subs.partymenu import PartyMenu


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
            SubScreen.PARTY_MENU,
        ):
            return event

        if hasattr(event, "x") or hasattr(event, "y"):
            return None  # Disables global mouse events
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
        return super().process_event(event)

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
            case SubScreen.PARTY_MENU:
                self.activate_party_menu()
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

    def activate_party_menu(self):
        self.game.info_log("Activating Party Menu...")
        self.game.set_sub_screen(SubScreen.PARTY_MENU)
        self.current_header = "Party Menu"
        self.scene.add_effect(PartyMenu(self.screen, self.game, self))
