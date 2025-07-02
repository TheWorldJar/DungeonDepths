from enum import Enum


class Attributes(Enum):
    """An actor's basic attributes"""

    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    ENDURANCE = "endurance"
    RESILIENCE = "resilience"
    INTELLIGENCE = "intelligence"
    WILLPOWER = "willpower"
    INTUITION = "intuition"
    PERCEPTION = "perception"


class CombatSkills(Enum):
    """An actor's combat skills"""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    DEFENCE = "defence"


class Actor:
    """Default Actor Parent Class"""

    def __init__(self, name: str, actor_type: str, health: int, abilities: set):
        self.name = name
        self.actor_type = actor_type
        self.max_health = health
        self.current_health = health
        self.abilities = abilities

    def use_ability(self):
        """Children of Actor need to define their own logic to use abilities"""
        raise NotImplementedError("Actor Error: 1000")

    def change_health(self, change: int):
        """Changes the actor's health"""
        self.current_health += change

    def get_type(self) -> str:
        return self.actor_type

    def get_health(self) -> int:
        return self.current_health
