class GameState:
    """Object to track the game's current state"""

    def __init__(self):
        self.current_scene = "Start"
        self.current_sub = None
        self.characters = []
        self.inventory = []
