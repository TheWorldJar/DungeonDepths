import random
from enum import Enum
from src.actors.actor import Actor, Attributes, CombatSkills
from ancestries import Ancestry
from classes import Classes


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
        if name is None or name == "":
            # Default name is Steve Dave. Replace with a proper name generator later.
            name = "Steve Dave"

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

        # Change starting attributes & skills based on class and ancestry
        self.char_class = char_class
        self.change_starting_attributes()

        # Calculate starting health
        health = (
            10
            + (self.attributes[Attributes.ENDURANCE] * 5)
            + (self.attributes[Attributes.RESILIENCE] * 5)
            + (self.attributes[Attributes.WILLPOWER] * 5)
        )

        # Get 4 abilities from the class list
        abilities = set()

        # Call parent constructor
        super().__init__(name, "character", health, abilities)

    def change_starting_attributes(self):
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
