from enum import Enum

from src.actors.ability import Ability


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
        self,
        name: str,
        actor_type: str,
        health: int,
        armour: int,
        abilities: set,
        attributes: dict,
        combat_skills: dict,
    ):
        self.name = name
        self.actor_type = actor_type
        self.max_health = health
        self.current_health = health
        self.armour = armour
        self.abilities = set()
        for a in abilities:
            self.abilities.add(
                Ability(
                    name=a.value["name"],
                    is_active=a.value["is_active"],
                    has_target=a.value["has_target"],
                    func=a.value["func"],
                    pref_targ=a.value["pref_targ"],
                    duration=a.value["duration"],
                )
            )
        self.effects = set()
        self.attributes = attributes
        self.combat_skills = combat_skills
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
        self.effects.add(effect)

    def remove_effect(self, effect):
        self.effects.remove(effect)

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
            "effects": self.effects,
        }
