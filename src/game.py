from actors.actor import Actor


class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        self.current_scene = "Start"
        self.current_sub = None
        self.characters = [Actor("Empty", "None", 0, 0, set())] * 8
        self.inventory = []
        self.slots = 2
