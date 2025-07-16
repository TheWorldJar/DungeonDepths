from enum import Enum

from src.const import NO_DURATION

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.roll import roll
from src.actors.ability import PrefTarget


def mind_over_matter(source: Actor):
    raise NotImplementedError


def glass_cannon(source: Actor):
    raise NotImplementedError


def reconstitute(source: Actor, target: Actor):
    heal = roll(
        source.attributes[Attributes.WILLPOWER]
        + source.combat_skills[CombatSkills.MAGIC]
    )[0]
    target.change_health(heal)


def dark_pact(source: Actor, target: Actor):
    raise NotImplementedError


def suppress(source: Actor, target: Actor):
    raise NotImplementedError


def eldritch_blast(source: Actor, target: Actor):
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


def shadow_pool(source: Actor, target: list[Actor]):
    for t in target:
        attack = roll(
            source.attributes[Attributes.STRENGTH]
            + source.combat_skills[CombatSkills.MELEE]
        )[0]
        defence = roll(t.combat_skills[CombatSkills.DEFENCE])[0] + t.get_armour()

        delta = attack - defence
        if delta >= 0:
            t.change_health(-(1 + (delta // 2)))


def arcane_bomb(source: Actor, target: Actor):
    raise NotImplementedError


class Occultist(Enum):
    MIND_OVER_MATTER = {
        "name": "mind_over_matter",
        "is_active": False,
        "has_target": False,
        "func": mind_over_matter,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    GLASS_CANNON = {
        "name": "glass_cannon",
        "is_active": False,
        "has_target": False,
        "func": glass_cannon,
        "pref_targ": PrefTarget.SELF,
        "duration": NO_DURATION,
    }
    RECONSTITUTE = {
        "name": "reconsitute",
        "is_active": True,
        "has_target": True,
        "func": reconstitute,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
    DARK_PACT = {
        "name": "dark_pact",
        "is_active": True,
        "has_target": True,
        "func": dark_pact,
        "pref_targ": PrefTarget.HIGH,
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
    ELDRITCH_BLAST = {
        "name": "eldritch_blast",
        "is_active": True,
        "has_target": True,
        "func": eldritch_blast,
        "pref_targ": PrefTarget.ANY,
        "duration": NO_DURATION,
    }
    SHADOW_POOL = {
        "name": "shadow_pool",
        "is_active": True,
        "has_target": True,
        "func": shadow_pool,
        "pref_targ": PrefTarget.ALL,
        "duration": NO_DURATION,
    }
    ARCANE_BOMB = {
        "name": "arcane_bomb",
        "is_active": True,
        "has_target": True,
        "func": arcane_bomb,
        "pref_targ": PrefTarget.LOW,
        "duration": NO_DURATION,
    }
