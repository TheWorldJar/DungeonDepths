from enum import Enum

from src.const import MARAUDER_BASE_REGEN, MARAUDER_HEALTH_MULTIPLIER

from src.actors.actor import Actor
from src.actors.roll import roll
from src.actors.characters.character import Character, Attributes, CombatSkills
from src.actors.ability import PrefTarget


def strongman(source: Character):
    source.max_health += (
        source.attributes[Attributes.STRENGTH] * MARAUDER_HEALTH_MULTIPLIER
    )


def regenerate(source: Character):
    source.change_health(
        MARAUDER_BASE_REGEN + roll(source.attributes[Attributes.RESILIENCE])[0]
    )


def cleave(source: Character, target: list[Actor]):
    for t in target:
        attack = roll(
            source.attributes[Attributes.STRENGTH]
            + source.combat_skills[CombatSkills.MELEE]
        )[0]
        defence = roll(t.combat_skills[CombatSkills.DEFENCE])[0] + t.get_armour()

        for e in source.effects:
            if hasattr(e, "empower") or hasattr(e, "weakness"):
                attack += e.value

        delta = attack - defence
        if delta >= 0:
            t.change_health(-(1 + delta))


def power_strike(source: Character, target: Actor):
    attack = roll(
        source.attributes[Attributes.STRENGTH]
        + source.combat_skills[CombatSkills.MELEE]
    )[0]
    defence = (
        roll(target.combat_skills[CombatSkills.DEFENCE])[0]
        + target.get_armour()
        + (target.attributes[Attributes.STRENGTH] // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_health(
            -(1 + delta + (source.attributes[Attributes.STRENGTH] // 3))
        )


def decapitate(source: Character, target: Actor):
    attack = roll(
        source.attributes[Attributes.STRENGTH]
        + source.combat_skills[CombatSkills.MELEE]
    )[0]
    defence = roll(target.combat_skills[CombatSkills.DEFENCE])[0] + target.get_armour()
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + delta))


def empower(source: Character):
    is_empowered = False
    for e in source.effects:
        if hasattr(e, "empower"):
            is_empowered = True
    if not is_empowered:
        source.add_effect("empower")  # This line is placehodler


def slam(source: Character, target: list[Actor]):
    for t in target:
        t.initiative -= roll(
            source.attributes[Attributes.RESILIENCE]
            + source.combat_skills[CombatSkills.MELEE]
        )[0]


def overkill(source: Character, target: Actor):
    attack = roll(
        source.attributes[Attributes.STRENGTH]
        + source.combat_skills[CombatSkills.MELEE]
    )[0]
    defence = roll(target.combat_skills[CombatSkills.DEFENCE])[0] + target.get_armour()
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + delta))


class Marauder(Enum):
    # (name, is_active, has_target, func, PrefTarget)
    STRONGMAN = ("strongman", False, False, strongman, PrefTarget.SELF)
    REGENERATE = ("regenerate", True, False, regenerate, PrefTarget.SELF)
    CLEAVE = ("cleave", True, True, cleave, PrefTarget.ANY)
    POWER_STRIKE = ("power strike", True, True, power_strike, PrefTarget.ANY)
    DECAPITATE = ("decapitate", True, True, decapitate, PrefTarget.FIRST)
    EMPOWER = ("empower", True, False, empower, PrefTarget.SELF)
    SLAM = ("slam", True, True, slam, PrefTarget.ANY)
    OVERKILL = ("overkill", True, True, overkill, PrefTarget.LOW)
