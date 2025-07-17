from enum import Enum

from src.const import NO_DURATION, SUCCESS_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def lay_on_hands(source: Actor, target: Actor):
    raise NotImplementedError


def holy_power(source: Actor):
    raise NotImplementedError


def smite(source: Actor, target: Actor):
    raise NotImplementedError


def punish(source: Actor, target: Actor):
    raise NotImplementedError


def leader(source: Actor):
    raise NotImplementedError


def contempt(source: Actor, target: Actor):
    raise NotImplementedError


def regenerate(source: Actor):
    raise NotImplementedError


def exorcism(source: Actor, target: list[Actor]):
    for t in target:
        attack = roll(
            source.get_attribute(Attributes.STRENGTH)
            + source.get_combat_skill(CombatSkills.MELEE)
        )[0]
        defence = roll(t.get_combat_skill(CombatSkills.DEFENCE))[0] + t.get_armour()
        delta = attack - defence
        if delta >= 0:
            t.change_current_health(-(1 + delta))


class Templar(Enum):
    LAY_ON_HANDS = {
        "name": "lay_on_hands",
        "is_active": True,
        "has_target": True,
        "func": lay_on_hands,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    HOLY_POWER = {
        "name": "holy_power",
        "is_active": True,
        "has_target": False,
        "func": holy_power,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    SMITE = {
        "name": "smite",
        "is_active": True,
        "has_target": True,
        "func": smite,
        "pref_targ": PrefTarget.HIGH,
        "duration": NO_DURATION,
    }
    PUNISH = {
        "name": "punish",
        "is_active": True,
        "has_target": True,
        "func": punish,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    LEADER = {
        "name": "leader",
        "is_active": False,
        "has_target": False,
        "func": leader,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    CONTEMPT = {
        "name": "contempt",
        "is_active": True,
        "has_target": True,
        "func": lay_on_hands,
        "pref_targ": PrefTarget.HIGH,
        "duration": SUCCESS_DURATION,
    }
    REGENERATE = {
        "name": "regenerate",
        "is_active": True,
        "has_target": False,
        "func": regenerate,
        "pref_targ": PrefTarget.SELF,
        "duration": SUCCESS_DURATION,
    }
    EXORCISM = {
        "name": "exorcism",
        "is_active": True,
        "has_target": True,
        "func": exorcism,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
