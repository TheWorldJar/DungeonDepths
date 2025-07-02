import random
from enum import Enum
from src.actors.actor import Actor
from src.actors.roll import roll
from src.actors.characters.character import Character, Attributes, CombatSkills

class Marauder(Enum):
    STRONGMAN = strongman(source, target)
    REGENERATE = regenerate(source, target)
    CLEAVE = cleave(source, target)
    POWER_STRIKE = 
    DECAPITATE = 
    EMPOWER = 
    SLAM = 
    CHAIN = 

def strongman(source: Character, target=None):
    source.max_health += source.attributes[Attributes.STRENGTH] * 3

def regenerate(source: Character, target=None):
    source.change_health(1 + roll(source.attributes[Attributes.RESILIENCE])[0])

def cleave(source: Character, target: list[Actor]):
    for t in target:
        t.change_health(roll(source.attributes[Attributes.STRENGTH] + source.combat_skills[CombatSkills.MELEE]))

def power_strike(source: Character, target: Actor):
    