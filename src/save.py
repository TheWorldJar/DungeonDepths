import os
import json

from src.const import SAVE_FILE, SAVE_PATH, DEBUG

from src.actors.characters.character import Character


def check_save(game_state) -> str | None:
    # If there is no save file directory, create it.
    if not os.path.exists(SAVE_PATH) or not os.path.isdir(SAVE_PATH):
        game_state.logger.info("Creating Save Folder...")
        os.makedirs(SAVE_PATH)

    # If there is a save.json file, try to load it.
    if os.path.exists(SAVE_FILE) and os.path.isfile(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as j:
                save = json.load(j)
        except ValueError:
            game_state.logger.warning("Save File is not Valid!")
            return None
        game_state.logger.info("Save File Found!")
        return save

    # Otherwise, create a blank save file.
    game_state.logger.info("Creating Blank Save...")
    data = {
        "current_scene": "Start",
        "current_sub": ("Defaul", 0),
        "characters": [],
        "inventory": [],
        "slots": 2,
        "is_empty_save": True,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as s:
        json.dump(data, s, indent=4)
    return None


def load_save(game_state, save):
    game_state.logger.info("Loading Save...")
    if DEBUG:
        game_state.logger.debug(save)
    char_data = []
    try:
        empty_save_data = save["is_empty_save"]
        if empty_save_data:
            game_state.logger.info("Aborting Loading: Save File is Empty!")
            return None
        scene_data = save["current_scene"]
        sub_data = save["current_sub"]
        slot_data = save["slots"]
        for i in range(0, slot_data):
            char_save_data = save["characters"][str(i)]
            char_data.append(Character.from_save(char_save_data))
        inv_data = save["inventory"]

    except KeyError:
        game_state.logger.warning("Aborting Loading: Save File is Malformed!")
        return None

    game_state.current_scene = scene_data
    game_state.current_sub = sub_data
    game_state.characters = char_data
    game_state.inventory = inv_data
    game_state.slots = slot_data
    game_state.is_empty_save = empty_save_data
    game_state.logger.info("Finished Loading Save")


def write_save(game_state):
    game_state.logger.info("Saving to Disk...")
    game_state.save_to_json()
