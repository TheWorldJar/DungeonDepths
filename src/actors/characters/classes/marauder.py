from enum import Enum

from src.const import (
    MARAUDER_BASE_REGEN,
    MARAUDER_HEALTH_MULTIPLIER,
    NO_DURATION,
    SUCCESS_DURATION,
)

from src.game_types import Attributes, CombatSkills

from src.actors.actor import Actor
from src.actors.roll import roll_target
from src.actors.ability import PrefTarget


def strongman(source: Actor):
    source.change_max_health(
        source.get_attribute(Attributes.STRENGTH) * MARAUDER_HEALTH_MULTIPLIER
    )


def regenerate(source: Actor):
    raise NotImplementedError


def cleave(source: Actor, target: list[Actor]):
    for t in target:
        attack = roll_target(
            source.get_attribute(Attributes.STRENGTH)
            + source.get_combat_skill(CombatSkills.MELEE)
        )[0]
        defence = (
            roll_target(t.get_combat_skill(CombatSkills.DEFENCE))[0] + t.get_armour()
        )

        delta = attack - defence
        if delta >= 0:
            t.change_current_health(-(1 + delta))


def power_strike(source: Actor, target: Actor):
    attack = roll_target(
        source.get_attribute(Attributes.STRENGTH)
        + source.get_combat_skill(CombatSkills.MELEE)
    )[0]
    defence = (
        roll_target(target.get_combat_skill(CombatSkills.DEFENCE))[0]
        + target.get_armour()
        + (target.get_attribute(Attributes.STRENGTH) // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(
            -(1 + delta + (source.get_attribute(Attributes.STRENGTH) // 3))
        )


def decapitate(source: Actor, target: Actor):
    attack = roll_target(
        source.get_attribute(Attributes.STRENGTH)
        + source.get_combat_skill(CombatSkills.MELEE)
    )[0]
    defence = (
        roll_target(target.get_combat_skill(CombatSkills.DEFENCE))[0]
        + target.get_armour()
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(-(1 + delta))


def empower(source: Actor):
    raise NotImplementedError


def slam(source: Actor, target: list[Actor]):
    for t in target:
        t.change_initiative(
            -(
                roll_target(
                    source.get_attribute(Attributes.RESILIENCE)
                    + source.get_combat_skill(CombatSkills.MELEE)
                )[0]
            )
        )


def overkill(source: Actor, target: Actor):
    attack = roll_target(
        source.get_attribute(Attributes.STRENGTH)
        + source.get_combat_skill(CombatSkills.MELEE)
    )[0]
    defence = (
        roll_target(target.get_combat_skill(CombatSkills.DEFENCE))[0]
        + target.get_armour()
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(-(1 + delta))


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
        "duration": SUCCESS_DURATION,
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
