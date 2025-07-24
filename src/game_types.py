from enum import Enum


class ActorType(Enum):
    NONE = "None"
    CHARACTER = "Character"
    MONSTER = "Monster"
    PUZZLE = "Puzzle"
    SUMMON = "Summon"


class Attributes(Enum):
    """An actor's basic attributes"""

    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    ENDURANCE = "endurance"
    RESILIENCE = "resilience"
    INTELLIGENCE = "intelligence"
    WILLPOWER = "willpower"
    INTUITION = "intuition"
    PERCEPTION = "perception"


class CombatSkills(Enum):
    """An actor's combat skills"""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    DEFENCE = "defence"


class CraftingSkills(Enum):
    """A character's crafting skills"""

    BLACKSMITHING = "blacksmithing"
    OUTFITTING = "outfitting"
    ENCHANTING = "enchanting"
    ALCHEMY = "alchemy"


class SecondarySkills(Enum):
    """A character's secondary skills"""

    FITNESS = "fitness"
    STEALTH = "stealth"
    SURVIVAL = "survival"
    MEDICINE = "medicine"
    NATURE = "nature"
    ENGINEERING = "engineering"
    OCCULTISM = "occultism"
    SPEECHCRAFT = "speechcraft"


class ItemType(Enum):
    HELMET = "helmet"
    CHESTPIECE = "chestpiece"
    GLOVES = "gloves"
    BOOTS = "boots"
    WEAPON = "weapon"
    RING = "ring"
    AMULET = "amulet"
