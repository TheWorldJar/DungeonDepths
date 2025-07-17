from enum import Enum

from src.const import NO_DURATION, NEXT_TURN_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def vigilance(source: Actor):
    raise NotImplementedError


def multistrike(source: Actor, target: Actor):
    raise NotImplementedError


def high_slash(source: Actor, target: Actor):
    attack = roll(
        source.get_attribute(Attributes.DEXTERITY)
        + source.get_combat_skill(CombatSkills.MELEE)
    )[0]
    defence = (
        roll(target.get_combat_skill(CombatSkills.DEFENCE))[0] + target.get_armour()
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(-(1 + delta))


def vengeance(source: Actor, target: Actor):
    raise NotImplementedError


def precise_strike(source: Actor, target: Actor):
    attack = roll(
        source.get_attribute(Attributes.DEXTERITY)
        + source.get_combat_skill(CombatSkills.MELEE)
    )[0]
    defence = (
        roll(target.get_combat_skill(CombatSkills.DEFENCE))[0]
        + target.get_armour()
        - (source.get_attribute(Attributes.DEXTERITY) // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(-(1 + (delta // 2)))


def critical_strike(source: Actor, target: Actor):
    raise NotImplementedError


def avoidance(source: Actor):
    raise NotImplementedError


def restitution(source: Actor, target: Actor):
    raise NotImplementedError


class Sentinel(Enum):
    VIGILANCE = {
        "name": "vigilance",
        "is_active": False,
        "has_target": False,
        "func": vigilance,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    MULTISTRIKE = {
        "name": "multistrike",
        "is_active": True,
        "has_target": True,
        "func": multistrike,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    HIGH_SLASH = {
        "name": "high_slash",
        "is_active": True,
        "has_target": True,
        "func": high_slash,
        "pref_targ": PrefTarget.NOT_LAST,
        "duration": NO_DURATION,
    }
    VENGEANCE = {
        "name": "vengeance",
        "is_active": True,
        "has_target": True,
        "func": vengeance,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    PRECISE_STRIKE = {
        "name": "preceise_strike",
        "is_active": True,
        "has_target": True,
        "func": precise_strike,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    CRITICAL_STRIKE = {
        "name": "critical_strike",
        "is_active": True,
        "has_target": True,
        "func": critical_strike,
        "pref_targ": PrefTarget.HIGH,
        "duration": NO_DURATION,
    }
    AVOIDANCE = {
        "name": "avoidance",
        "is_active": True,
        "has_target": False,
        "func": avoidance,
        "pref_targ": PrefTarget.SELF,
        "duration": NEXT_TURN_DURATION,
    }
    RESTITUTION = {
        "name": "restitution",
        "is_active": True,
        "has_target": True,
        "func": restitution,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
