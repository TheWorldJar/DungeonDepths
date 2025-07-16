from enum import Enum

from src.const import NO_DURATION, SUCCESS_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def martyr(source: Actor, target: Actor):
    heal = roll(
        source.attributes[Attributes.RESILIENCE]
        + source.combat_skills[CombatSkills.DEFENCE]
    )[0]
    target.change_health(heal)
    source.change_health(-(heal))


def passion(source: Actor):
    raise NotImplementedError


def chain_heal(source: Actor, target: Actor):
    raise NotImplementedError


def suppress(source: Actor, target: Actor):
    raise NotImplementedError


def lightning_bolt(source: Actor, target: Actor):
    attack = roll(
        source.attributes[Attributes.INTELLIGENCE]
        + source.combat_skills[CombatSkills.MAGIC]
    )[0]
    defence = (
        roll(target.combat_skills[CombatSkills.DEFENCE])[0]
        + target.get_armour()
        - (source.attributes[Attributes.DEXTERITY] // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_health(-(1 + (delta // 2)))


def radiance(source: Actor):
    raise NotImplementedError


def ball_lightning(source: Actor, target: Actor):
    attack = roll(
        source.attributes[Attributes.INTELLIGENCE]
        + source.combat_skills[CombatSkills.MAGIC]
    )[0]
    defence = (
        roll(target.combat_skills[CombatSkills.DEFENCE])[0]
        + target.get_armour()
        + (target.attributes[Attributes.INTELLIGENCE] // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_health(
            -(1 + delta + (source.attributes[Attributes.INTELLIGENCE] // 3))
        )


def meditate(source: Actor):
    raise NotImplementedError


class Cenobite(Enum):
    MARTYR = {
        "name": "martyr",
        "is_active": True,
        "has_target": True,
        "func": martyr,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    PASSION = {
        "name": "passion",
        "is_active": False,
        "has_target": False,
        "func": passion,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    CHAIN_HEAL = {
        "name": "chain_heal",
        "is_active": True,
        "has_target": True,
        "func": chain_heal,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    SUPPRESS = {
        "name": "suppress",
        "is_active": True,
        "has_target": True,
        "func": suppress,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    LIGHTNING_BOLT = {
        "name": "lightning_bolt",
        "is_active": True,
        "has_target": True,
        "func": lightning_bolt,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    RADIANCE = {
        "name": "radiance",
        "is_active": False,
        "has_target": False,
        "func": radiance,
        "pref_targ": PrefTarget.SELF,
        "duration": SUCCESS_DURATION,
    }
    BALL_LIGHTNING = {
        "name": "ball_lightning",
        "is_active": True,
        "has_target": True,
        "func": ball_lightning,
        "pref_targ": PrefTarget.HIGH,
        "duration": NO_DURATION,
    }
    MEDITATE = {
        "name": "meditate",
        "is_active": True,
        "has_target": False,
        "func": meditate,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
