from enum import Enum

from src.const import NO_DURATION, SUCCESS_DURATION, NEXT_TURN_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def dextrous(source: Actor):
    raise NotImplementedError


def perceptive(source: Actor):
    raise NotImplementedError


def avoidance(source: Actor):
    # Dexterity
    # Reduce Next Damage
    raise NotImplementedError


def take_aim(source: Actor):
    # Perception
    # Increase Next Perception Roll
    raise NotImplementedError


def strangle(source: Actor, target: Actor):
    attack = roll(
        source.attributes[Attributes.PERCEPTION]
        + source.combat_skills[CombatSkills.RANGED]
    )[0]
    defence = roll(target.combat_skills[CombatSkills.DEFENCE])[0] + target.get_armour()
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + delta))


def puncture(source: Actor, target: list[Actor]):
    # Dexterity
    # Bleed 2 Targets
    raise NotImplementedError


def mark(source: Actor, target: Actor):
    # Perception
    # Normal Damage. Target is higher priority.
    raise NotImplementedError


def rapid_fire(source: Actor, target: Actor):
    # Dexterity
    # Reduced damage, but 50% chance to repeat until chance fails.
    raise NotImplementedError


class Stalker(Enum):
    # (name, is_active, has_target, func, PrefTarget, duration)
    DEXTROUS = {
        "name": "dextrous",
        "is_active": False,
        "has_target": False,
        "func": dextrous,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    PERCEPTIVE = {
        "name": "perceptive",
        "is_active": False,
        "has_target": False,
        "func": perceptive,
        "pref_targ": PrefTarget.SELF,
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
    TAKE_AIM = {
        "name": "take_aim",
        "is_active": True,
        "has_target": False,
        "func": take_aim,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    STRANGLE = {
        "name": "strangle",
        "is_active": True,
        "has_target": True,
        "func": strangle,
        "pref_targ": PrefTarget.LAST,
        "duration": NO_DURATION,
    }
    PUNCTURE = {
        "name": "puncture",
        "is_active": True,
        "has_target": True,
        "func": puncture,
        "pref_targ": PrefTarget.ANY,
        "duration": SUCCESS_DURATION,
    }
    MARK = {
        "name": "mark",
        "is_active": True,
        "has_target": True,
        "func": mark,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    RAPID_FIRE = {
        "name": "rapid_fire",
        "is_active": True,
        "has_target": True,
        "func": rapid_fire,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
