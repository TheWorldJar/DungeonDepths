import logging
import os
import json

from src.const import MAX_CHARACTER_SLOT, START_CHARACTER_SLOT, DEBUG, SAVE_FILE

from src.actors.characters.character import Character
from src.actors.characters.classes.classes import Classes


class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        self.current_scene = "Start"
        self.current_sub = ("Default", 0)
        self.characters = [Character(Classes.MARAUDER, "Empty")] * MAX_CHARACTER_SLOT
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

    def save_to_json(self):
        current_scene = {"current_scene": self.current_scene}
        current_sub = {"current_sub": self.current_sub}
        char_in_slot = {}
        for i, c in enumerate(self.characters):
            char_in_slot[i] = c.to_json()
        characters = {"characters": char_in_slot}

        # Placeholder for inventory
        inventory = {"inventory": self.inventory}
        slots = {"slots": self.slots}

        save_data = {**current_scene, **current_sub, **characters, **inventory, **slots}
        if DEBUG:
            self.logger.debug(save_data)

        with open(SAVE_FILE, "w", encoding="utf-8") as s:
            json.dump(save_data, s, indent=4)
