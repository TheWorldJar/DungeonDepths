from enum import Enum
from src.actors.actor import Actor
from src.actors.roll import roll
from src.actors.characters.character import Character, Attributes, CombatSkills


def strongman(source: Character):
    source.max_health += source.attributes[Attributes.STRENGTH] * 3


def regenerate(source: Character):
    source.change_health(1 + roll(source.attributes[Attributes.RESILIENCE])[0])


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
    STRONGMAN = ("strongman", strongman)
    REGENERATE = ("regenerate", regenerate)
    CLEAVE = ("cleave", cleave)
    POWER_STRIKE = ("power strike", power_strike)
    DECAPITATE = ("decapitate", decapitate)
    EMPOWER = ("empower", empower)
    SLAM = ("slam", slam)
    OVERKILL = ("overkill", overkill)
