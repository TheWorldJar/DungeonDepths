from enum import Enum

from src.const import MARAUDER_BASE_REGEN, MARAUDER_HEALTH_MULTIPLIER, NO_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def strongman(source: Actor):
    source.max_health += (
        source.attributes[Attributes.STRENGTH] * MARAUDER_HEALTH_MULTIPLIER
    )


def regenerate(source: Actor):
    source.change_health(
        MARAUDER_BASE_REGEN + roll(source.attributes[Attributes.RESILIENCE])[0]
    )


def cleave(source: Actor, target: list[Actor]):
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


def power_strike(source: Actor, target: Actor):
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


def decapitate(source: Actor, target: Actor):
    attack = roll(
        source.attributes[Attributes.STRENGTH]
        + source.combat_skills[CombatSkills.MELEE]
    )[0]
    defence = roll(target.combat_skills[CombatSkills.DEFENCE])[0] + target.get_armour()
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + delta))


def empower(source: Actor):
    raise NotImplementedError


def slam(source: Actor, target: list[Actor]):
    for t in target:
        t.initiative -= roll(
            source.attributes[Attributes.RESILIENCE]
            + source.combat_skills[CombatSkills.MELEE]
        )[0]


def overkill(source: Actor, target: Actor):
    attack = roll(
        source.attributes[Attributes.STRENGTH]
        + source.combat_skills[CombatSkills.MELEE]
    )[0]
    defence = roll(target.combat_skills[CombatSkills.DEFENCE])[0] + target.get_armour()
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + delta))


class Marauder(Enum):
    # (name, is_active, has_target, func, PrefTarget, duration)
    STRONGMAN = {
        "name": "strongman",
        "is_active": False,
        "has_target": False,
        "func": strongman,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    REGENERATE = {
        "name": "regenerate",
        "is_active": True,
        "has_target": False,
        "func": regenerate,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    CLEAVE = {
        "name": "cleave",
        "is_active": True,
        "has_target": True,
        "func": cleave,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    POWER_STRIKE = {
        "name": "power_strike",
        "is_active": True,
        "has_target": True,
        "func": power_strike,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    DECAPITATE = {
        "name": "decapitate",
        "is_active": True,
        "has_target": True,
        "func": decapitate,
        "pref_targ": PrefTarget.FIRST,
        "duration": NO_DURATION,
    }
    EMPOWER = {
        "name": "empower",
        "is_active": True,
        "has_target": False,
        "func": empower,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    SLAM = {
        "name": "slam",
        "is_active": True,
        "has_target": True,
        "func": slam,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    OVERKILL = {
        "name": "overkill",
        "is_active": True,
        "has_target": True,
        "func": overkill,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
