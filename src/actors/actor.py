from enum import Enum

from src.actors.ability import Ability
from src.actors.status import Status


class ActorType(Enum):
    NONE = "None"
    CHARACTER = "Character"
    MONSTER = "Monster"
    PUZZLE = "Puzzle"
    SUMMON = "Summon"


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
        actor_type: ActorType,
        health: int,
        armour: int,
        abilities: list,
        attributes: dict,
        combat_skills: dict,
    ):
        self._name = name
        self._actor_type = actor_type
        self._max_health = health
        self._current_health = health
        self._armour = armour
        self._abilities: list[Ability] = []
        for a in abilities:
            self.add_ability(
                Ability(
                    name=a.value["name"],
                    is_active=a.value["is_active"],
                    has_target=a.value["has_target"],
                    func=a.value["func"],
                    pref_targ=a.value["pref_targ"],
                    duration=a.value["duration"],
                )
            )
        self._effects: list[Status] = []
        self._attributes = attributes
        self._combat_skills = combat_skills
        self._initiative = 0

    def to_json(self):
        abilities_data = {}
        for i, a in enumerate(self.get_all_abilities()):
            abilities_data[i] = a.to_json()

        attributes_data = {}
        for t in self.get_all_attributes():
            attributes_data[t.name] = self.get_attribute(t)

        combat_skills_data = {}
        for c in self.get_all_combat_skills():
            combat_skills_data[c.name] = self.get_combat_skill(c)

        return {
            "name": self.get_name(),
            "actor_type": self.get_actor_type().value.upper(),
            "max_health": self.get_max_health(),
            "current_health": self.get_current_health(),
            "armour": self.get_armour(),
            "abilities": abilities_data,
            "attributes": attributes_data,
            "combat_skills": combat_skills_data,
        }

    # Nothing but getters and setters below this line

    # _name
    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    # _actor_type
    def get_actor_type(self) -> ActorType:
        return self._actor_type

    def set_actor_type(self, actor_type: ActorType):
        self._actor_type = actor_type

    # _max_health
    def get_max_health(self) -> int:
        return self._max_health

    def set_max_health(self, health: int):
        self._max_health = health

    def change_max_health(self, change: int):
        self._max_health += change

    # _current_health
    def get_current_health(self) -> int:
        return self._current_health

    def set_current_health(self, health: int):
        self._current_health = health

    def change_current_health(self, change: int):
        self._current_health += change

    # _armour
    def get_armour(self) -> int:
        return self._armour

    def set_armour(self, armour: int):
        self._armour = armour

    def change_armour(self, change: int):
        self._armour += change

    # _abilities
    def get_ability(self, slot: int) -> Ability:
        return self._abilities[slot]

    def get_all_abilities(self) -> list[Ability]:
        return self._abilities

    def set_ability(self, ability: Ability, slot):
        self._abilities[slot] = ability

    def add_ability(self, ability: Ability):
        if len(self.get_all_abilities()) >= 4:
            return
        self._abilities.append(ability)

    def remove_ability(self, slot):
        self._abilities.pop(slot)

    def clear_abilities(self):
        self._abilities.clear()

    # _effects
    def get_effect(self, slot: int) -> Status:
        return self._effects[slot]

    def get_all_effects(self) -> list[Status]:
        return self._effects

    def set_effect(self, effect: Status, slot: int):
        self._effects[slot] = effect

    def add_effect(self, effect: Status):
        self._effects.append(effect)

    def remove_effect(self, slot):
        self._effects.pop(slot)

    def clear_effects(self):
        self._effects.clear()

    # _attributes
    def get_attribute(self, attribute: Attributes) -> int:
        return self._attributes[attribute]

    def get_all_attributes(self) -> dict:
        return self._attributes

    def set_attribute(self, attribute: Attributes, value: int):
        self._attributes[attribute] = value

    def change_attribute(self, attribute: Attributes, change: int):
        self._attributes[attribute] += change

    # _combat_skills
    def get_combat_skill(self, skill: CombatSkills) -> int:
        return self._combat_skills[skill]

    def get_all_combat_skills(self) -> dict:
        return self._combat_skills

    def set_combat_skill(self, skill: CombatSkills, value: int):
        self._combat_skills[skill] = value

    def change_combat_skill(self, skill: CombatSkills, change: int):
        self._combat_skills[skill] += change

    # _initiative
    def get_initiative(self) -> int:
        return self._initiative

    def set_initiative(self, value: int):
        self._initiative = value

    def change_initiative(self, change: int):
        self._initiative += change
