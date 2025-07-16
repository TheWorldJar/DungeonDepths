import random
from enum import Enum

from src.const import CHARACTER_BASE_HEALTH, CHARACTER_HEALTH_MULTIPLIER, ABILITY_SLOT

from src.actors.actor import Actor, Attributes, CombatSkills
from src.actors.characters.ancestries import Ancestry

from src.actors.characters.classes.classes import Classes
from src.actors.characters.classes.marauder import Marauder
from src.actors.characters.classes.stalker import Stalker
from src.actors.characters.classes.occultist import Occultist
from src.actors.characters.classes.penitent import Penitent
from src.actors.characters.classes.primalist import Primalist
from src.actors.characters.classes.sentinel import Sentinel
from src.actors.characters.classes.templar import Templar
from src.actors.characters.classes.cenobite import Cenobite


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
        for e in self.effects:
            e.execute(self)

    @classmethod
    def from_save(cls, data: dict):
        new_character = cls(Classes.MARAUDER, "New")
        new_character.name = data["name"]
        new_character.actor_type = data["actor_type"]
        new_character.max_health = data["max_health"]
        new_character.current_health = data["current_health"]
        new_character.armour = data["armour"]
        for attribute_name, attribute_value in data["attributes"].items():
            attr_enum_member = Attributes[attribute_name]
            new_character.attributes[attr_enum_member] = attribute_value
        for combat_skill_name, combat_skill_value in data["combat_skills"].items():
            combat_enum_member = CombatSkills[combat_skill_name]
            new_character.combat_skills[combat_enum_member] = combat_skill_value
        anc_enum_member = Ancestry[data["ancestry"]]
        new_character.ancestry = anc_enum_member
        char_class_enum_member = Classes[data["class"]]
        new_character.char_class = char_class_enum_member

        new_character.abilities.clear()
        for _, ability_name in data["abilities"].items():
            match new_character.char_class:
                case Classes.MARAUDER:
                    ability_enum_member = Marauder[ability_name]
                case _:
                    raise NotImplementedError
            ability_data = ability_enum_member.value
            new_character.abilities.add(
                Ability(
                    name=ability_data["name"],
                    is_active=ability_data["is_active"],
                    has_target=ability_data["has_target"],
                    func=ability_data["func"],
                    pref_targ=ability_data["pref_targ"],
                    duration=ability_data["duration"],
                )
            )

        for crafting_skill_name, crafting_skill_value in data[
            "crafting_skills"
        ].items():
            craft_enum_member = CraftingSkills[crafting_skill_name]
            new_character.crafting_skills[craft_enum_member] = crafting_skill_value
        for secondary_skill_name, secondary_skill_value in data[
            "secondary_skills"
        ].items():
            secondary_enum_member = SecondarySkills[secondary_skill_name]
            new_character.secondary_skills[secondary_enum_member] = (
                secondary_skill_value
            )
        return new_character

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
            case Classes.SENTINEL:
                return set(random.sample(list(Sentinel), ABILITY_SLOT))
            case Classes.STALKER:
                return set(random.sample(list(Stalker), ABILITY_SLOT))
            case Classes.TEMPLAR:
                return set(random.sample(list(Templar), ABILITY_SLOT))
            case Classes.PRIMALIST:
                return set(random.sample(list(Primalist), ABILITY_SLOT))
            case Classes.OCCULTIST:
                return set(random.sample(list(Occultist), ABILITY_SLOT))
            case Classes.CENOBITE:
                return set(random.sample(list(Cenobite), ABILITY_SLOT))
            case Classes.PENITENT:
                return set(random.sample(list(Penitent), ABILITY_SLOT))

    def to_json(self):
        crafting_skills_data = {}
        for c in self.crafting_skills:
            crafting_skills_data[c.name] = self.crafting_skills[c]

        secondary_skills_data = {}
        for s in self.secondary_skills:
            secondary_skills_data[s.name] = self.secondary_skills[s]

        char_data = {
            "ancestry": self.ancestry.name,
            "class": self.char_class.name,
            "crafting_skills": crafting_skills_data,
            "secondary_skills": secondary_skills_data,
        }
        return {**super().to_json(), **char_data}
