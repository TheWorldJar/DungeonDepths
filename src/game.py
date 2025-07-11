import logging
import os

from src.const import MAX_CHARACTER_SLOT, START_CHARACTER_SLOT, DEBUG

from src.actors.actor import Actor


class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        self.current_scene = "Start"
        self.current_sub = ("Default", 0)
        self.characters = [
            Actor("Empty", "None", 0, 0, set(), {}, {})
        ] * MAX_CHARACTER_SLOT
        self.inventory = []
        self.slots = START_CHARACTER_SLOT
        if DEBUG:
            if os.path.exists(os.path.realpath("debug.log")):
                os.remove(os.path.realpath("debug.log"))
            logging.basicConfig(
                filename="debug.log",
                encoding="utf-8",
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger("game_state")
