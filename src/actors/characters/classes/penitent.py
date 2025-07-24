from enum import Enum

from src.const import NO_DURATION

from src.game_types import Attributes, CombatSkills

from src.actors.actor import Actor
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def thorn_crown(source: Actor):
    raise NotImplementedError


def scarification(source: Actor):
    raise NotImplementedError


def flagelation(source: Actor):
    raise NotImplementedError


def selfless(source: Actor):
    raise NotImplementedError


def inspire(source: Actor, target: list[Actor]):
    for t in target:
        heal = (
            roll(
                source.get_attribute(Attributes.RESILIENCE)
                + source.get_combat_skill(CombatSkills.DEFENCE)
            )[0]
        ) // 2
        t.change_current_health(heal)


def punish(source: Actor, target: Actor):
    raise NotImplementedError


def transferance(source: Actor, target: Actor):
    raise NotImplementedError


def martyr(source: Actor, target: Actor):
    heal = roll(
        source.get_attribute(Attributes.RESILIENCE)
        + source.get_combat_skill(CombatSkills.DEFENCE)
    )[0]
    target.change_current_health(heal)
    source.change_current_health(-(heal))


class Penitent(Enum):
    THORN_CROWN = {
        "name": "thorn_crown",
        "is_active": False,
        "has_target": False,
        "func": thorn_crown,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    SCARIFICATION = {
        "name": "scarification",
        "is_active": False,
        "has_target": False,
        "func": scarification,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    FLAGELATION = {
        "name": "flagelation",
        "is_active": False,
        "has_target": False,
        "func": flagelation,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    SELFLESS = {
        "name": "selfless",
        "is_active": False,
        "has_target": False,
        "func": selfless,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    INSPIRE = {
        "name": "inspire",
        "is_active": True,
        "has_target": True,
        "func": inspire,
        "pref_targ": PrefTarget.ALL,
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
    TRANSFERANCE = {
        "name": "transferance",
        "is_active": True,
        "has_target": True,
        "func": transferance,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    MARTYR = {
        "name": "martyr",
        "is_active": True,
        "has_target": True,
        "func": martyr,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
