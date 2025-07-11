import random
from enum import Enum

from src.const import CHARACTER_BASE_HEALTH, CHARACTER_HEALTH_MULTIPLIER, ABILITY_SLOT

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.characters.ancestries import Ancestry
from src.actors.characters.classes.classes import Classes
from src.actors.characters.classes.marauder import Marauder
from src.actors.ability import Ability, PrefTarget


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
        attributes = {
            Attributes.STRENGTH: 1,
            Attributes.DEXTERITY: 1,
            Attributes.ENDURANCE: 1,
            Attributes.RESILIENCE: 1,
            Attributes.INTELLIGENCE: 1,
            Attributes.WILLPOWER: 1,
            Attributes.INTUITION: 1,
            Attributes.PERCEPTION: 1,
        }

        combat_skills = {
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
            SecondarySkills.SURVIVAL: 0,
            SecondarySkills.MEDICINE: 0,
            SecondarySkills.NATURE: 0,
            SecondarySkills.ENGINEERING: 0,
            SecondarySkills.OCCULTISM: 0,
            SecondarySkills.SPEECHCRAFT: 0,
        }

        # Generate a race at random.
        self.ancestry = random.choice(list(Ancestry))
        self._change_on_ancestry(attributes)

        # Change starting attributes & skills based on class and ancestry
        self.char_class = char_class
        self._change_on_class(attributes, combat_skills)

        # Calculate starting health
        health = (
            CHARACTER_BASE_HEALTH
            + (attributes[Attributes.ENDURANCE] * CHARACTER_HEALTH_MULTIPLIER)
            + (attributes[Attributes.RESILIENCE] * CHARACTER_HEALTH_MULTIPLIER)
            + (attributes[Attributes.WILLPOWER] * CHARACTER_HEALTH_MULTIPLIER)
        )

        # Get 4 abilities from the class list
        abilities = self._get_initial_abilities()

        # Call parent constructor
        super().__init__(
            name, "character", health, 0, abilities, attributes, combat_skills
        )

        # Check for Passive Ability effects
        for a in self.abilities:
            if not a.is_active and a.pref_targ == PrefTarget.SELF:
                a.apply(self)

    def _change_on_ancestry(self, attributes):
        match self.ancestry:
            case Ancestry.HUMAN:
                attributes[Attributes.INTUITION] += 1
                attributes[Attributes.RESILIENCE] += 1
            case Ancestry.NEPHILIM:
                attributes[Attributes.INTELLIGENCE] += 1
                attributes[Attributes.ENDURANCE] += 1
            case Ancestry.ELF:
                attributes[Attributes.DEXTERITY] += 1
                attributes[Attributes.PERCEPTION] += 1
            case Ancestry.DRAGONKIN:
                attributes[Attributes.STRENGTH] += 1
                attributes[Attributes.WILLPOWER] += 1

    def _change_on_class(self, attributes, combat_skills):
        match self.char_class:
            case Classes.MARAUDER:
                attributes[Attributes.STRENGTH] += 1
                attributes[Attributes.RESILIENCE] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.BLACKSMITHING] += 1
                self.secondary_skills[SecondarySkills.SURVIVAL] += 1
            case Classes.SENTINEL:
                attributes[Attributes.DEXTERITY] += 1
                attributes[Attributes.INTUITION] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.OUTFITTING] += 1
                self.secondary_skills[SecondarySkills.SPEECHCRAFT] += 1
            case Classes.STALKER:
                attributes[Attributes.DEXTERITY] += 1
                attributes[Attributes.PERCEPTION] += 1
                combat_skills[CombatSkills.RANGED] += 1
                self.crafting_skills[CraftingSkills.OUTFITTING] += 1
                self.secondary_skills[SecondarySkills.STEALTH] += 1
            case Classes.TEMPLAR:
                attributes[Attributes.STRENGTH] += 1
                attributes[Attributes.WILLPOWER] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.crafting_skills[CraftingSkills.BLACKSMITHING] += 1
                self.secondary_skills[SecondarySkills.FITNESS] += 1
            case Classes.PRIMALIST:
                attributes[Attributes.PERCEPTION] += 1
                attributes[Attributes.INTUITION] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ENCHANTING] += 1
                self.secondary_skills[SecondarySkills.NATURE] += 1
            case Classes.OCCULTIST:
                attributes[Attributes.INTELLIGENCE] += 1
                attributes[Attributes.WILLPOWER] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ENCHANTING] += 1
                self.secondary_skills[SecondarySkills.OCCULTISM] += 1
            case Classes.CENOBITE:
                attributes[Attributes.INTELLIGENCE] += 1
                attributes[Attributes.ENDURANCE] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.crafting_skills[CraftingSkills.ALCHEMY] += 1
                self.secondary_skills[SecondarySkills.ENGINEERING] += 1
            case Classes.PENITENT:
                attributes[Attributes.ENDURANCE] += 1
                attributes[Attributes.RESILIENCE] += 1
                combat_skills[CombatSkills.DEFENCE] += 1
                self.crafting_skills[CraftingSkills.ALCHEMY] += 1
                self.secondary_skills[SecondarySkills.MEDICINE] += 1

    def _get_initial_abilities(self) -> set:
        match self.char_class:
            case Classes.MARAUDER:
                return set(random.sample(list(Marauder), ABILITY_SLOT))
            case _:
                raise NotImplementedError()

    def to_json(self):
        char_data = {
            "ancestry": self.ancestry,
            "class": self.char_class,
            "crafting_skills": self.crafting_skills,
            "secondary_skills": self.secondary_skills,
        }
        return {**super().to_json(), **char_data}
