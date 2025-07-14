import os

from asciimatics.effects import Print
from asciimatics.renderers import SpeechBubble
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import PopUpDialog

from src.const import MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH, SAVE_FILE, PALETTE
from src.save import set_save_status

from src.scenes.compositions.screensize import print_screen_size
from src.scenes.compositions.topbar import print_top_bar


class DeletePopup(PopUpDialog):
    def __init__(self, screen, game_state):
        self.game = game_state
        super().__init__(
            screen,
            "Really Delete the Save?",
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
        try:
            self.game.logger.info("Deleting Save File...")
            os.remove(SAVE_FILE)
            self.game.logger.info("Save File Deleted!")
        except Exception as e:
            self.game.logger.warning(f"Unknown Exception While Deleting Save File: {e}")
        set_save_status(self.game)
        self.screen.clear_buffer(0, 0, 0)

    def _cancel(self):
        self.screen.clear_buffer(0, 0, 0)


class ManageEffect(Print):
    """The Game's Manage Savegame Screen"""

    def __init__(self, screen, game_state):
        self.game = game_state

        # This is only for initilization.
        super().__init__(
            screen=screen,
            renderer=SpeechBubble("Copyright (c) 2025, TheWorldJar"),
            y=screen.height - 4,
        )

    def process_event(self, event):
        if hasattr(event, "key_code"):
            if event.key_code in (ord("b"), ord("B")):  # Press 'b' to go back
                self.game.current_scene = "Start"
                raise NextScene("Start")
            if event.key_code in (ord("q"), ord("Q")):
                return None  # Disables global exit from this screen.
            if event.key_code in (ord("\n"), ord("\r")):
                return None  # Disables global scene cycling.
            if event.key_code in (ord("d"), ord("D")):
                self.activate_delete_confirm()
        return event

    def _update(self, frame_no):
        if (
            self.screen.width < MIN_SCREEN_WIDTH
            or self.screen.height < MIN_SCREEN_HEIGHT
        ):
            print_screen_size(self)
        else:
            # Draw the top bar
            print_top_bar(self, "Manage Save")

            line1 = "Save File Status: "
            self.screen.print_at(
                text=line1,
                x=(self.screen.width - len(line1 + self.game.save_status)) // 2,
                y=self.screen.height // 3,
                colour=Screen.COLOUR_WHITE,
                attr=Screen.A_BOLD,
            )
            match self.game.save_status:
                case "Valid":
                    save_status_colour = Screen.COLOUR_GREEN
                    line2 = f"Save File Location: {SAVE_FILE}"
                case "Malformed":
                    save_status_colour = Screen.COLOUR_MAGENTA
                    line2 = "Your save file is missing a required key! Entering the play area will overwrite it!"
                case "Empty":
                    save_status_colour = Screen.COLOUR_YELLOW
                    line2 = "Your save file is empty and can be safely overriden!"
                case "Invalid":
                    save_status_colour = Screen.COLOUR_RED
                    line2 = "Your save file is not a valid JSON file!"

            self.screen.print_at(
                text=self.game.save_status,
                x=(self.screen.width - len(line1 + self.game.save_status)) // 2
                + len(line1),
                y=self.screen.height // 3,
                colour=Screen.COLOUR_BLACK,
                attr=Screen.A_UNDERLINE,
                bg=save_status_colour,
            )
            self.screen.print_at(
                text=line2,
                x=(self.screen.width - len(line2)) // 2,
                y=self.screen.height // 3 + 1,
                colour=save_status_colour,
                attr=Screen.A_BOLD,
            )
            line3 = "SaveFile Stats:"
            self.screen.print_at(
                text=line3,
                x=(self.screen.width - len(line3)) // 2,
                y=self.screen.height // 3 + 2,
                colour=Screen.COLOUR_WHITE,
                attr=Screen.A_UNDERLINE,
            )
            self.screen.print_at(
                text="Placeholder!",
                x=(self.screen.width - len(line3)) // 2,
                y=self.screen.height // 3 + 3,
                colour=Screen.COLOUR_WHITE,
                attr=Screen.A_BOLD,
            )
            line4 = "[D]elete Save File?"
            colour_map = [
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            ]
            colour_map += [
                (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            ] * (
                len(line4) - 3
            )  # The first 3 characters have already been defined above.
            self.screen.paint(
                text=line4,
                x=(self.screen.width - len(line4)) // 2,
                y=self.screen.height // 3 + 6,
                colour_map=colour_map,
            )
            line5 = "[B]ack to the Main Menu"
            colour_map = [
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                (Screen.COLOUR_YELLOW, Screen.A_UNDERLINE, Screen.COLOUR_BLACK),
                (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
            ]
            colour_map += [
                (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            ] * (
                len(line5) - 3
            )  # The first 3 characters have already been defined above.
            self.screen.paint(
                text=line5,
                x=(self.screen.width - len(line5)) // 2,
                y=self.screen.height - 3,
                colour_map=colour_map,
            )

    def activate_delete_confirm(self):
        self.scene.add_effect(DeletePopup(self.screen, self.game))
