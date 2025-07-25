import logging
import os
import json

from enum import Enum

from src.const import (
    MAX_CHARACTER_SLOT,
    START_CHARACTER_SLOT,
    DEBUG,
    SAVE_FILE,
    START_SCENE,
    PLAY_SCENE,
    SETTINGS_SCENE,
    WARRANTY_SCENE,
    LICENSE_SCENE,
    MANAGE_SAVE_SCENE,
)

from src.game_types import ActorType
from src.actors.characters.character import Character
from src.actors.characters.classes.classes import Classes


class SubScreen(Enum):
    # Global Subs
    DEFAULT = "Default"
    QUIT = "Quit"

    # Play Scene Subs
    CHAR_CREATION = "Char_Creation"
    GUIDE = "Guide"
    ACTIVITY_MENU = "Activity_Menu"
    CHARACTER_SHEET = "Character_Sheet"
    PARTY_MENU = "Party_Menu"
    DUNGEON_MENU = "Dungeon_Menu"
    COMBAT_SCREEN = "Combat_Screen"
    EQUIP_MENU = "Equip_Menu"
    COMBAT_TRAIN = "Combat_Train"
    CRAFTING_MENU = "Crafting_Menu"
    SECONDARY_TRAIN = "Secondary_Train"
    INVENTORY = "Inventory"
    CHAR_DISMISS = "Char_Dismiss"

    # Other Scene Subs Go Here.


class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        # These values are saved to file.
        self._current_scene = START_SCENE
        self._current_sub = (SubScreen.DEFAULT, 0)
        self._characters = [Character(Classes.MARAUDER, "Empty")] * MAX_CHARACTER_SLOT
        for character in self._characters:
            character.set_actor_type(ActorType.NONE)
        self._inventory = []
        self._slots = START_CHARACTER_SLOT
        self.is_empty_save = True

        # These values are not saved to file.
        if DEBUG:
            if os.path.exists(os.path.realpath("debug.log")):
                os.remove(os.path.realpath("debug.log"))
            logging.basicConfig(
                filename="debug.log",
                encoding="utf-8",
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            self._logger = logging.getLogger("game_state")
        else:
            if os.path.exists(os.path.realpath("debug.log")):
                os.remove(os.path.realpath("debug.log"))
            logging.basicConfig(
                filename="debug.log",
                encoding="utf-8",
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            self._logger = logging.getLogger("game_state")
        self.save_status = "Empty"  # Helper functions in the Save module

    def reset(self):
        self.set_scene(START_SCENE)
        self.set_sub((SubScreen.DEFAULT, 0))
        self._characters = [Character(Classes.MARAUDER, "Empty")] * MAX_CHARACTER_SLOT
        for character in self._characters:
            character.set_actor_type(ActorType.NONE)
        self._inventory = []
        self.set_slots(START_CHARACTER_SLOT)
        self.is_empty_save = True
        self.save_status = "Empty"

    def save_to_json(self):
        current_scene = {"current_scene": self.get_scene()}
        current_sub = {"current_sub": [self.get_sub_screen().name, self.get_sub_data()]}
        char_in_slot = {}
        for i, c in enumerate(self.get_all_characters()):
            char_in_slot[i] = c.to_json()
        characters = {"characters": char_in_slot}

        # Placeholder for inventory
        inventory = {"inventory": self.get_all_inventory()}
        slots = {"slots": self.get_slots()}
        empty_save = {"is_empty_save": self.is_empty_save}

        save_data = {
            **current_scene,
            **current_sub,
            **characters,
            **inventory,
            **slots,
            **empty_save,
        }
        self.debug_log(save_data)

        with open(SAVE_FILE, "w", encoding="utf-8") as s:
            json.dump(save_data, s, indent=4)

    def debug_log(self, log: str):
        if DEBUG:
            self._logger.debug(log)

    def info_log(self, log: str):
        self._logger.info(log)

    def warn_log(self, log: str):
        self._logger.warning(log)

    def err_log(self, log: str):
        self._logger.error(log)

    # Nothing but getters and setters below this line

    # _current Scene
    def get_scene(self) -> str:
        return self._current_scene

    def set_scene(self, scene: str):
        if scene not in (
            START_SCENE,
            PLAY_SCENE,
            SETTINGS_SCENE,
            MANAGE_SAVE_SCENE,
            WARRANTY_SCENE,
            LICENSE_SCENE,
        ):
            self.warn_log("Unknown Scene: Switching to Main Menu Instead...")
            self._current_scene = START_SCENE
        else:
            self.debug_log(f"Setting Current Scene: {scene}")
            self._current_scene = scene

    # _current Sub
    def get_sub(self) -> tuple[SubScreen, int]:
        return self._current_sub

    def get_sub_screen(self) -> SubScreen:
        return self._current_sub[0]

    def get_sub_data(self) -> int:
        return self._current_sub[1]

    def set_sub(self, sub: tuple[SubScreen, int]):
        self.debug_log(f"Setting Current Sub: {sub}")
        self._current_sub = sub

    def set_sub_screen(self, sub: SubScreen):
        self.debug_log(f"Setting Current Sub Screen: {sub}")
        self._current_sub = (sub, self.get_sub_data())

    def set_sub_data(self, data: int):
        self.debug_log(f"Setting Current Sub Screen: {data}")
        self._current_sub = (self.get_sub_screen(), data)

    # _characters
    def get_character(self, slot: int) -> Character:
        return self._characters[slot]

    def get_all_characters(self) -> list[Character]:
        return self._characters

    def set_character(self, character: Character, slot: int):
        self.debug_log(f"Setting Character[{slot}]: {Character}")
        self._characters[slot] = character

    # _inventory
    # Update when the rest of the inventory system is implemented
    def get_item(self, slot: int):
        return self._inventory[slot]

    def get_all_inventory(self):
        return self._inventory

    def set_item(self, item, slot):
        self.debug_log(f"Setting Inventory[{slot}]: {item}")
        self._inventory[slot] = item

    def add_item(self, item):
        self.debug_log(f"Adding to Inventory: {item}")
        self._inventory.append(item)

    def remove_item(self, slot):
        self.debug_log(f"Removing Inventory[{slot}]")
        self._inventory.pop(slot)

    # _slots
    def get_slots(self) -> int:
        return self._slots

    def set_slots(self, slots: int):
        self.debug_log(f"Setting Slots: {slots}")
        self._slots = slots
