import random
from enum import Enum

from src.const import CHARACTER_BASE_HEALTH, CHARACTER_HEALTH_MULTIPLIER

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.characters.ancestries import Ancestry
from src.actors.characters.classes.classes import Classes


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
    MEDICINE = "medicine"
    SURVIVAL = "survival"
    ENGINEERING = "engineering"
    OCCULTISM = "occultism"
    SPEECHCRAFT = "speechcraft"
    NATURE = "nature"


class Character(Actor):
    def __init__(
        self,
        char_class: Classes,
        name=None,
    ):

        # Generate the character's name.
        # Though the CharacterCreationView should always give us a name, this prevents any fuckery from happening anywhere.
        if name is None or name == "":
            # Default name is Nameless. Replace with a proper name generator later.
            name = "Nameless"

        # Prepare the character's default attributes and skills.
        self.attributes = {
            Attributes.STRENGTH: 1,
            Attributes.DEXTERITY: 1,
            Attributes.ENDURANCE: 1,
            Attributes.RESILIENCE: 1,
            Attributes.INTELLIGENCE: 1,
            Attributes.WILLPOWER: 1,
            Attributes.INTUITION: 1,
            Attributes.PERCEPTION: 1,
        }

        self.combat_skills = {
            CombatSkills.MELEE: 0,
            CombatSkills.RANGED: 0,
            CombatSkills.MAGIC: 0,
            CombatSkills.DEFENCE: 0,
        }

        self.crafting_skills = {
            CraftingSkills.BLACKSMITHING: 0,
            CraftingSkills.OUTFITTING: 0,
            CraftingSkills.ENCHANTING: 0,
            CraftingSkills.ALCHEMY: 0,
        }

        self.secondary_skills = {
            SecondarySkills.FITNESS: 0,
            SecondarySkills.STEALTH: 0,
            SecondarySkills.MEDICINE: 0,
            SecondarySkills.SURVIVAL: 0,
            SecondarySkills.ENGINEERING: 0,
            SecondarySkills.OCCULTISM: 0,
            SecondarySkills.SPEECHCRAFT: 0,
            SecondarySkills.NATURE: 0,
        }

        # Generate a race at random.
        self.ancestry = random.choice(list(Ancestry))
        self.change_on_ancestry()

        # Change starting attributes & skills based on class and ancestry
        self.char_class = char_class
        self.change_on_class()

        # Calculate starting health
        health = (
            CHARACTER_BASE_HEALTH
            + (self.attributes[Attributes.ENDURANCE] * CHARACTER_HEALTH_MULTIPLIER)
            + (self.attributes[Attributes.RESILIENCE] * CHARACTER_HEALTH_MULTIPLIER)
            + (self.attributes[Attributes.WILLPOWER] * CHARACTER_HEALTH_MULTIPLIER)
        )

        # Get 4 abilities from the class list
        # To Be Implemented.
        abilities = set()

        # Call parent constructor
        super().__init__(name, "character", health, 0, abilities)

    def change_on_ancestry(self):
        match self.ancestry:
            case Ancestry.HUMAN:
                self.attributes[Attributes.INTUITION] += 1
                self.attributes[Attributes.RESILIENCE] += 1
            case Ancestry.NEPHILIM:
                self.attributes[Attributes.INTELLIGENCE] += 1
                self.attributes[Attributes.ENDURANCE] += 1
            case Ancestry.ELF:
                self.attributes[Attributes.DEXTERITY] += 1
                self.attributes[Attributes.PERCEPTION] += 1
            case Ancestry.DRAGONKIN:
                self.attributes[Attributes.STRENGTH] += 1
                self.attributes[Attributes.WILLPOWER] += 1

    def change_on_class(self):
        match self.char_class:
            case Classes.MARAUDER:
                self.attributes[Attributes.STRENGTH] += 1
                self.attributes[Attributes.RESILIENCE] += 1
                self.combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.BLACKSMITHING] += 1
                self.secondary_skills[SecondarySkills.SURVIVAL] += 1
            case Classes.STALKER:
                self.attributes[Attributes.DEXTERITY] += 1
                self.attributes[Attributes.PERCEPTION] += 1
                self.combat_skills[CombatSkills.RANGED] += 1
                self.crafting_skills[CraftingSkills.OUTFITTING] += 1
                self.secondary_skills[SecondarySkills.STEALTH] += 1
            case Classes.OCCULTIST:
                self.attributes[Attributes.INTELLIGENCE] += 1
                self.attributes[Attributes.WILLPOWER] += 1
                self.combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ENCHANTING] += 1
                self.secondary_skills[SecondarySkills.OCCULTISM] += 1
            case Classes.PENITENT:
                self.attributes[Attributes.ENDURANCE] += 1
                self.attributes[Attributes.RESILIENCE] += 1
                self.combat_skills[CombatSkills.DEFENCE] += 1
                self.crafting_skills[CraftingSkills.ALCHEMY] += 1
                self.secondary_skills[SecondarySkills.MEDICINE] += 1
            case Classes.PRIMALIST:
                self.attributes[Attributes.PERCEPTION] += 1
                self.attributes[Attributes.INTUITION] += 1
                self.combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ENCHANTING] += 1
                self.secondary_skills[SecondarySkills.NATURE] += 1
            case Classes.SENTINEL:
                self.attributes[Attributes.DEXTERITY] += 1
                self.attributes[Attributes.INTUITION] += 1
                self.combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.OUTFITTING] += 1
                self.secondary_skills[SecondarySkills.SPEECHCRAFT] += 1
            case Classes.TEMPLAR:
                self.attributes[Attributes.STRENGTH] += 1
                self.attributes[Attributes.WILLPOWER] += 1
                self.combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.BLACKSMITHING] += 1
                self.secondary_skills[SecondarySkills.FITNESS] += 1
            case Classes.CENOBITE:
                self.attributes[Attributes.INTELLIGENCE] += 1
                self.attributes[Attributes.ENDURANCE] += 1
                self.combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ALCHEMY] += 1
                self.secondary_skills[SecondarySkills.ENGINEERING] += 1

    def to_json(self):
        return {
            "name": self.name,
            "actor_type": self.actor_type,
            "health": self.max_health,
            "armour": self.armour,
            "ancestry": self.ancestry,
            "class": self.char_class,
            "abilities": self.abilities,
            "attributes": self.attributes,
            "combat_skills": self.combat_skills,
            "crafting_skills": self.crafting_skills,
            "secondary_skills": self.secondary_skills,
        }
