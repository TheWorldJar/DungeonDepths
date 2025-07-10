from src.const import MAX_CHARACTER_SLOT, START_CHARACTER_SLOT

from src.actors.actor import Actor


class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        self.current_scene = "Start"
        self.current_sub = ("Default", 0)
        self.characters = [Actor("Empty", "None", 0, 0, set())] * MAX_CHARACTER_SLOT
        self.inventory = []
        self.slots = START_CHARACTER_SLOT
