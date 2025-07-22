from enum import Enum

from src.actors.actor import Actor
from src.actors.characters.classes.classes import Classes
from src.actors.characters.character import (
    CraftingSkills,
    CombatSkills,
    Attributes,
    SecondarySkills,
)


class ItemType(Enum):
    HELMET = "helmet"
    CHESTPIECE = "chestpiece"
    GLOVES = "gloves"
    BOOTS = "boots"
    WEAPON = "weapon"
    RING = "ring"
    AMULET = "amulet"


def rat_amulet(source: Actor):
    raise NotImplementedError


class T0Gear(Enum):
    # Helmets
    LINEN_VEIL = {
        "name": "linen_veil",
        "type": ItemType.HELMET,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE, Classes.OCCULTIST, Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    BONE_MASK = {
        "name": "bone_mask",
        "type": ItemType.HELMET,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST, Classes.SENTINEL, Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    LEAD_CAP = {
        "name": "lead_cap",
        "type": ItemType.HELMET,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER, Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    # Chestpieces
    LINEN_VESTMENTS = {
        "name": "linen_vestments",
        "type": ItemType.CHESTPIECE,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE, Classes.OCCULTIST, Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    BONE_VEST = {
        "name": "bone_vest",
        "type": ItemType.CHESTPIECE,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST, Classes.SENTINEL, Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    LEAD_DISK = {
        "name": "lead_disk",
        "type": ItemType.CHESTPIECE,
        "stat": "armour",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER, Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    # Gloves
    LINEN_GLOVES = {
        "name": "linen_gloves",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.MAGIC,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE, Classes.OCCULTIST],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    LINEN_WRAPS = {
        "name": "linen_wraps",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.MELEE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    BONE_BRACELETS = {
        "name": "bone_bracelets",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.MAGIC,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    BONE_GLOVES = {
        "name": "bone_gloves",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.MELEE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.SENTINEL],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    BONE_VAMBRACES = {
        "name": "bone_vambraces",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.RANGED,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    LEAD_KNUCKLES = {
        "name": "lead_knuckles",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.MELEE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    LEAD_VAMBRACES = {
        "name": "lead_vambraces",
        "type": ItemType.GLOVES,
        "stat": CombatSkills.DEFENCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    # Boots
    STRAW_SANDALS = {
        "name": "straw_sandals",
        "type": ItemType.BOOTS,
        "stat": "initiative",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE, Classes.OCCULTIST, Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    BONE_GRIEVES = {
        "name": "bone_grieves",
        "type": ItemType.BOOTS,
        "stat": "initiative",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST, Classes.SENTINEL, Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    LEAD_GRIEVES = {
        "name": "lead_grieves",
        "type": ItemType.BOOTS,
        "stat": "initiative",
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER, Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    # Weapons
    DUSTY_TOME = {
        "name": "dusty_tome",
        "type": ItemType.WEAPON,
        "stat": Attributes.INTELLIGENCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.OCCULTIST],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    DUSTY_ORB = {
        "name": "dusty_orb",
        "type": ItemType.WEAPON,
        "stat": Attributes.WILLPOWER,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.OCCULTIST],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    DUSTY_ROD = {
        "name": "dusty_rod",
        "type": ItemType.WEAPON,
        "stat": Attributes.PERCEPTION,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    DUSTY_RITUAL_DAGGER = {
        "name": "dusty_ritual_dagger",
        "type": ItemType.WEAPON,
        "stat": Attributes.INTUITION,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PRIMALIST],
        "recipe": {},
        "craft": CraftingSkills.ENCHANTING,
        "sell": 1,
    }

    OLD_STAFF = {
        "name": "old_staff",
        "type": ItemType.WEAPON,
        "stat": Attributes.INTELLIGENCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    OLD_WHIP = {
        "name": "old_whip",
        "type": ItemType.WEAPON,
        "stat": Attributes.ENDURANCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.CENOBITE, Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    OLD_CLUB = {
        "name": "old_club",
        "type": ItemType.WEAPON,
        "stat": Attributes.RESILIENCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.PENITENT],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    OLD_SHORTBOW = {
        "name": "old_shortbow",
        "type": ItemType.WEAPON,
        "stat": Attributes.DEXTERITY,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    OLD_LONGBOW = {
        "name": "old_longbow",
        "type": ItemType.WEAPON,
        "stat": Attributes.PERCEPTION,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.STALKER],
        "recipe": {},
        "craft": CraftingSkills.OUTFITTING,
        "sell": 1,
    }

    RUSTY_MAUL = {
        "name": "rusty_maul",
        "type": ItemType.WEAPON,
        "stat": Attributes.STRENGTH,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER, Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    RUSTY_GREATAXE = {
        "name": "rusty_greataxe",
        "type": ItemType.WEAPON,
        "stat": Attributes.RESILIENCE,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.MARAUDER],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    RUSTY_LONGSWORD = {
        "name": "rusty_longsword",
        "type": ItemType.WEAPON,
        "stat": Attributes.DEXTERITY,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.SENTINEL],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    RUSTY_TWIN_DAGGERS = {
        "name": "rusty_twin_daggers",
        "type": ItemType.WEAPON,
        "stat": Attributes.INTUITION,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.SENTINEL],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    RUSTY_MACE_AND_SHIELD = {
        "name": "rusty_mace_and_shield",
        "type": ItemType.WEAPON,
        "stat": Attributes.WILLPOWER,
        "value": 1,
        "effect": None,
        "tier": 0,
        "class": [Classes.TEMPLAR],
        "recipe": {},
        "craft": CraftingSkills.BLACKSMITHING,
        "sell": 1,
    }

    # Rings
    LEAD_RING = {
        "name": "lead_ring",
        "type": ItemType.RING,
        "stat": list(SecondarySkills),
        "value": 1,
        "effect": "random",
        "tier": 0,
        "class": list(Classes),
        "recipe": {},
        "craft": CraftingSkills.ALCHEMY,
        "sell": 1,
    }

    # Amulets
    RAT_AMULET = {
        "name": "rat_amulet",
        "type": ItemType.AMULET,
        "stat": None,
        "value": 1,
        "effect": rat_amulet,
        "tier": 0,
        "class": list(Classes),
        "recipe": {},
        "craft": CraftingSkills.ALCHEMY,
        "sell": 1,
    }
