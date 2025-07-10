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

    def __init__(
        self, name: str, actor_type: str, health: int, armour: int, abilities: set
    ):
        self.name = name
        self.actor_type = actor_type
        self.max_health = health
        self.current_health = health
        self.armour = armour
        self.abilities = abilities
        self.effects = []
        self.initiative = 0

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

    def get_armour(self) -> int:
        return self.armour

    def add_effect(self, effect):
        self.effects.append(effect)

    def on_target(self):
        return self

    def to_json(self):
        return {
            "name": self.name,
            "actor_type": self.actor_type,
            "max_health": self.max_health,
            "current_health": self.current_health,
            "armour": self.armour,
            "abilities": self.abilities,
        }
