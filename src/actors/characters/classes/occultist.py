from enum import Enum

from src.const import NO_DURATION

from src.game_types import Attributes, CombatSkills

from src.actors.actor import Actor
from src.actors.roll import roll_target
from src.actors.ability import PrefTarget


def mind_over_matter(source: Actor):
    raise NotImplementedError


def glass_cannon(source: Actor):
    raise NotImplementedError


def reconstitute(source: Actor, target: Actor):
    heal = roll_target(
        source.get_attribute(Attributes.WILLPOWER)
        + source.get_combat_skill(CombatSkills.MAGIC)
    )[0]
    target.change_current_health(heal)


def dark_pact(source: Actor, target: Actor):
    raise NotImplementedError


def suppress(source: Actor, target: Actor):
    raise NotImplementedError


def eldritch_blast(source: Actor, target: Actor):
    attack = roll_target(
        source.get_attribute(Attributes.INTELLIGENCE)
        + source.get_combat_skill(CombatSkills.MAGIC)
    )[0]
    defence = (
        roll_target(target.get_combat_skill(CombatSkills.DEFENCE))[0]
        + target.get_armour()
        + (target.get_attribute(Attributes.INTELLIGENCE) // 3)
    )
    delta = attack - defence
    if delta >= 0:
        target.change_current_health(
            -(1 + delta + (source.get_attribute(Attributes.INTELLIGENCE) // 3))
        )


def shadow_pool(source: Actor, target: list[Actor]):
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
            t.change_current_health(-(1 + (delta // 2)))


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
