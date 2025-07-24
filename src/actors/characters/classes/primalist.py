from enum import Enum

from src.const import NO_DURATION, SUCCESS_DURATION

from src.game_types import Attributes, CombatSkills

from src.actors.actor import Actor
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def spider_totem(source: Actor):
    raise NotImplementedError


def snake_totem(source: Actor):
    raise NotImplementedError


def vulture_totem(source: Actor):
    raise NotImplementedError


def grasping_roots(source: Actor, target: list[Actor]):
    for t in target:
        t.change_initiative(
            -(
                roll(
                    source.get_attribute(Attributes.PERCEPTION)
                    + source.get_combat_skill(CombatSkills.MAGIC)
                )[0]
            )
        )


def vitality_totem(source: Actor, target: list[Actor]):
    raise NotImplementedError


def poison_spray(source: Actor, target: list[Actor]):
    raise NotImplementedError


def summon_wolf(source: Actor):
    raise NotImplementedError


def rock_bite(source: Actor, target: Actor):
    attack = roll(
        source.get_attribute(Attributes.PERCEPTION)
        + source.get_combat_skill(CombatSkills.MAGIC)
    )[0]
    defence = (
        roll(target.get_combat_skill(CombatSkills.DEFENCE))[0] + target.get_armour()
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(-(1 + delta))


class Primalist(Enum):
    SPIDER_TOTEM = {
        "name": "spider_totem",
        "is_active": False,
        "has_target": False,
        "func": spider_totem,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    SNAKE_TOTEM = {
        "name": "snake_totem",
        "is_active": False,
        "has_target": False,
        "func": snake_totem,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    VULTURE_TOTEN = {
        "name": "vulture_totem",
        "is_active": False,
        "has_target": False,
        "func": vulture_totem,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    GRASPING_ROOTS = {
        "name": "grasping_roots",
        "is_active": True,
        "has_target": True,
        "func": grasping_roots,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    VITALITY_TOTEM = {
        "name": "vitality_totem",
        "is_active": True,
        "has_target": True,
        "func": vitality_totem,
        "pref_targ": PrefTarget.ALL,
        "duration": SUCCESS_DURATION,
    }
    POISON_SPRAY = {
        "name": "poison_spray",
        "is_active": True,
        "has_target": True,
        "func": poison_spray,
        "pref_targ": PrefTarget.ANY,
        "duration": SUCCESS_DURATION,
    }
    SUMMON_WOLF = {
        "name": "summon_wolf",
        "is_active": True,
        "has_target": True,
        "func": summon_wolf,
        "pref_targ": PrefTarget.SELF,
        "duration": SUCCESS_DURATION,
    }
    ROCK_BITE = {
        "name": "rock_bite",
        "is_active": True,
        "has_target": True,
        "func": rock_bite,
        "pref_targ": PrefTarget.NOT_FIRST,
        "duration": NO_DURATION,
    }
