import os
import json

from src.const import SAVE_FILE, SAVE_PATH, START_SCENE, START_CHARACTER_SLOT
from src.game import GameState

from src.game import SubScreen
from src.actors.characters.character import Character


def check_save(game_state: GameState) -> str | None:
    # If there is no save file directory, create it.
    if not os.path.exists(SAVE_PATH) or not os.path.isdir(SAVE_PATH):
        game_state.info_log("Creating Save Folder...")
        os.makedirs(SAVE_PATH)

    # If there is no save.json file, create a blank save file.
    if not os.path.exists(SAVE_FILE) or not os.path.isfile(SAVE_FILE):
        game_state.info_log("Creating Blank Save...")
        data = {
            "current_scene": START_SCENE,
            "current_sub": (SubScreen.DEFAULT.name, 0),
            "characters": [],
            "inventory": [],
            "slots": START_CHARACTER_SLOT,
            "is_empty_save": True,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as s:
            json.dump(data, s, indent=4)

    # Return the save, even if it is empty.
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as j:
            save = json.load(j)
    except ValueError:
        game_state.warn_log("Save File is not Valid!")
        return None
    game_state.info_log("Save File Found!")
    return save


def load_save(game_state: GameState, save):
    empty_save_data = is_empty_save(game_state, save)
    if empty_save_data:
        game_state.reset()
        return None
    try:
        scene_data, sub_data, char_data, inv_data, slot_data = validate_save(
            game_state, save
        )
    except TypeError as e:
        game_state.warn_log(f"Aborting Loading: Save File is Malformed! Exception: {e}")
        return None

    if (
        scene_data is None
        or sub_data is None
        or char_data is None
        or inv_data is None
        or slot_data is None
    ):
        game_state.info_log("Something is wrong with the save's data!")
        return None
    game_state.info_log("Loading Save...")
    game_state.set_scene(scene_data)
    game_state.set_sub(sub_data)
    for i, c in enumerate(char_data):
        game_state.set_character(c, i)
    for item in inv_data:
        game_state.add_item(item)
    game_state.set_slots(slot_data)
    game_state.is_empty_save = empty_save_data
    game_state.set_party()
    game_state.info_log("Finished Loading Save")


def validate_save(game_state: GameState, save):
    game_state.info_log("Validating Save...")
    game_state.debug_log(save)
    char_data = []
    try:
        scene_data = save["current_scene"]
        sub = save["current_sub"]
        sub_enum_member = SubScreen[sub[0]]
        sub_data = (sub_enum_member, sub[1])
        slot_data = save["slots"]
        for i in range(0, slot_data):
            char_save_data = save["characters"][str(i)]
            game_state.debug_log(char_save_data)
            char_data.append(Character.from_save(char_save_data))
        inv_data = save["inventory"]

    except KeyError as e:
        game_state.warn_log(f"Aborting Loading: Save File is Malformed! Exception: {e}")
        return None

    return scene_data, sub_data, char_data, inv_data, slot_data


def is_empty_save(game_state: GameState, save):
    try:
        empty_save_data = save["is_empty_save"]
    except KeyError:
        game_state.info_log("Aborting Loading: Save File is Empty!")
        return True
    if empty_save_data:
        game_state.info_log("Aborting Loading: Save File is Empty!")
    return empty_save_data


def set_save_status(game_state: GameState):
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
    game_state.debug_log(save_status)
    game_state.save_status = save_status


def write_save(game_state: GameState):
    game_state.info_log("Saving to Disk...")
    game_state.save_to_json()
