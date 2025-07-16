import os
import json

from src.const import SAVE_FILE, SAVE_PATH, DEBUG

from src.game import SubScreen
from src.actors.characters.character import Character


def check_save(game_state) -> str | None:
    # If there is no save file directory, create it.
    if not os.path.exists(SAVE_PATH) or not os.path.isdir(SAVE_PATH):
        game_state.logger.info("Creating Save Folder...")
        os.makedirs(SAVE_PATH)

    # If there is no save.json file, create a blank save file.
    if not os.path.exists(SAVE_FILE) or not os.path.isfile(SAVE_FILE):
        game_state.logger.info("Creating Blank Save...")
        data = {
            "current_scene": "Start",
            "current_sub": ("Default", 0),
            "characters": [],
            "inventory": [],
            "slots": 2,
            "is_empty_save": True,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as s:
            json.dump(data, s, indent=4)

    # Return the save, even if it is empty.
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as j:
            save = json.load(j)
    except ValueError:
        game_state.logger.warning("Save File is not Valid!")
        return None
    game_state.logger.info("Save File Found!")
    return save


def load_save(game_state, save):
    empty_save_data = is_empty_save(game_state, save)
    if empty_save_data:
        game_state.reset()
        return None
    scene_data, sub_data, char_data, inv_data, slot_data = validate_save(
        game_state, save
    )
    game_state.logger.info("Loading Save...")
    game_state.current_scene = scene_data
    game_state.current_sub = sub_data
    game_state.characters = char_data
    game_state.inventory = inv_data
    game_state.slots = slot_data
    game_state.is_empty_save = empty_save_data
    game_state.logger.info("Finished Loading Save")


def validate_save(game_state, save):
    game_state.logger.info("Validating Save...")
    if DEBUG:
        game_state.logger.debug(save)
    char_data = []
    try:
        scene_data = save["current_scene"]
        sub, data = save["current_sub"].items()
        sub_enum_member = SubScreen[sub]
        sub_data = (sub_enum_member, data)
        slot_data = save["slots"]
        for i in range(0, slot_data):
            char_save_data = save["characters"][str(i)]
            char_data.append(Character.from_save(char_save_data))
        inv_data = save["inventory"]

    except KeyError as e:
        game_state.logger.warning(
            f"Aborting Loading: Save File is Malformed! Exception: {e}"
        )
        return None

    return scene_data, sub_data, char_data, inv_data, slot_data


def is_empty_save(game_state, save):
    try:
        empty_save_data = save["is_empty_save"]
    except KeyError:
        game_state.logger.info("Aborting Loading: Save File is Empty!")
        return True
    if empty_save_data:
        game_state.logger.info("Aborting Loading: Save File is Empty!")
    return empty_save_data


def set_save_status(game_state):
    save_status = "Empty"
    save = check_save(game_state)
    if save is None:
        save_status = "Invalid"
    else:
        if is_empty_save(game_state, save):
            save_status = "Empty"
        elif validate_save(game_state, save) is None:
            save_status = "Malformed"
        else:
            save_status = "Valid"
    game_state.logger.debug(save_status)
    game_state.save_status = save_status


def write_save(game_state):
    game_state.logger.info("Saving to Disk...")
    game_state.save_to_json()
