import random

from src.const import CHARACTER_BASE_HEALTH, CHARACTER_HEALTH_MULTIPLIER, ABILITY_SLOT

from src.game_types import (
    ActorType,
    Attributes,
    CombatSkills,
    CraftingSkills,
    SecondarySkills,
    ItemType,
)

from src.actors.actor import Actor

from src.actors.ability import Ability

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

from src.equipment.equipment import Equipment


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

        self._crafting_skills = {
            CraftingSkills.BLACKSMITHING: 0,
            CraftingSkills.OUTFITTING: 0,
            CraftingSkills.ENCHANTING: 0,
            CraftingSkills.ALCHEMY: 0,
        }

        self._secondary_skills = {
            SecondarySkills.FITNESS: 0,
            SecondarySkills.STEALTH: 0,
            SecondarySkills.SURVIVAL: 0,
            SecondarySkills.MEDICINE: 0,
            SecondarySkills.NATURE: 0,
            SecondarySkills.ENGINEERING: 0,
            SecondarySkills.OCCULTISM: 0,
            SecondarySkills.SPEECHCRAFT: 0,
        }

        self._equipment = {
            ItemType.HELMET: None,
            ItemType.CHESTPIECE: None,
            ItemType.GLOVES: None,
            ItemType.BOOTS: None,
            ItemType.WEAPON: None,
            ItemType.AMULET: None,
            ItemType.RING: {"left": None, "right": None},
        }

        # Generate a race at random.
        self._ancestry = random.choice(list(Ancestry))
        self._change_on_ancestry(attributes)

        # Change starting attributes and skills based on class
        self._char_class = char_class
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
            name, ActorType.CHARACTER, health, 0, abilities, attributes, combat_skills
        )

        self._enhanced_crafting_skills = self._crafting_skills.copy()
        self._enhanced_secondary_skills = self._secondary_skills.copy()

        # Find the correct starting gear and apply it
        self._get_initial_gear()

        # Check for Passive Ability effects

    @classmethod
    def from_save(cls, data: dict):
        new_character = cls(Classes.MARAUDER, "New")
        new_character.set_name(data["name"])
        new_character.set_actor_type(ActorType[data["actor_type"]])
        new_character.set_max_health(data["max_health"])
        new_character.set_current_health(data["current_health"])
        new_character.set_armour(data["armour"])
        for attribute_name, attribute_value in data["attributes"].items():
            attr_enum_member = Attributes[attribute_name]
            new_character.set_attribute(attr_enum_member, attribute_value)
            new_character.set_enhanced_attribute(attr_enum_member, attribute_value)
        for combat_skill_name, combat_skill_value in data["combat_skills"].items():
            combat_enum_member = CombatSkills[combat_skill_name]
            new_character.set_combat_skill(combat_enum_member, combat_skill_value)
            new_character.set_enhanced_combat_skill(
                combat_enum_member, combat_skill_value
            )
        new_character.set_ancestry(Ancestry[data["ancestry"]])
        new_character.set_char_class(Classes[data["class"]])
        new_character.set_initiative_mod(data["initiative_mod"])

        new_character.clear_abilities()
        for _, ability_name in data["abilities"].items():
            match new_character.get_char_class():
                case Classes.MARAUDER:
                    ability_enum_member = Marauder[ability_name]
                case Classes.SENTINEL:
                    ability_enum_member = Sentinel[ability_name]
                case Classes.STALKER:
                    ability_enum_member = Stalker[ability_name]
                case Classes.TEMPLAR:
                    ability_enum_member = Templar[ability_name]
                case Classes.PRIMALIST:
                    ability_enum_member = Primalist[ability_name]
                case Classes.OCCULTIST:
                    ability_enum_member = Occultist[ability_name]
                case Classes.CENOBITE:
                    ability_enum_member = Cenobite[ability_name]
                case Classes.PENITENT:
                    ability_enum_member = Penitent[ability_name]
            ability_data = ability_enum_member.value
            new_character.add_ability(
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
            new_character.set_crafting_skill(craft_enum_member, crafting_skill_value)
            new_character.set_enhanced_crafting_skill(
                craft_enum_member, crafting_skill_value
            )
        for secondary_skill_name, secondary_skill_value in data[
            "secondary_skills"
        ].items():
            secondary_enum_member = SecondarySkills[secondary_skill_name]
            new_character.set_secondary_skill(
                secondary_enum_member, secondary_skill_value
            )
            new_character.set_enhanced_secondary_skill(
                secondary_enum_member, secondary_skill_value
            )

        for slot, item in data["equipment"].items():
            item_type_enum_member = ItemType[slot]
            if item_type_enum_member == ItemType.RING:
                new_character.equip_gear(Equipment(item["left"]), "left")
                new_character.equip_gear(Equipment(item["right"]), "right")
            else:
                new_character.equip_gear(Equipment(item))

        return new_character

    def _change_on_ancestry(self, attributes):
        match self.get_ancestry():
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
        match self.get_char_class():
            case Classes.MARAUDER:
                attributes[Attributes.STRENGTH] += 1
                attributes[Attributes.RESILIENCE] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.change_crafting_skill(CraftingSkills.BLACKSMITHING, 1)
                self.change_secondary_skill(SecondarySkills.SURVIVAL, 1)
            case Classes.SENTINEL:
                attributes[Attributes.DEXTERITY] += 1
                attributes[Attributes.INTUITION] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.change_crafting_skill(CraftingSkills.OUTFITTING, 1)
                self.change_secondary_skill(SecondarySkills.SPEECHCRAFT, 1)
            case Classes.STALKER:
                attributes[Attributes.DEXTERITY] += 1
                attributes[Attributes.PERCEPTION] += 1
                combat_skills[CombatSkills.RANGED] += 1
                self.change_crafting_skill(CraftingSkills.OUTFITTING, 1)
                self.change_secondary_skill(SecondarySkills.STEALTH, 1)
            case Classes.TEMPLAR:
                attributes[Attributes.STRENGTH] += 1
                attributes[Attributes.WILLPOWER] += 1
                combat_skills[CombatSkills.MELEE] += 1
                self.change_crafting_skill(CraftingSkills.BLACKSMITHING, 1)
                self.change_secondary_skill(SecondarySkills.FITNESS, 1)
            case Classes.PRIMALIST:
                attributes[Attributes.PERCEPTION] += 1
                attributes[Attributes.INTUITION] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.change_crafting_skill(CraftingSkills.ENCHANTING, 1)
                self.change_secondary_skill(SecondarySkills.NATURE, 1)
            case Classes.OCCULTIST:
                attributes[Attributes.INTELLIGENCE] += 1
                attributes[Attributes.WILLPOWER] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.change_crafting_skill(CraftingSkills.ENCHANTING, 1)
                self.change_secondary_skill(SecondarySkills.OCCULTISM, 1)
            case Classes.CENOBITE:
                attributes[Attributes.INTELLIGENCE] += 1
                attributes[Attributes.ENDURANCE] += 1
                combat_skills[CombatSkills.MAGIC] += 1
                self.change_crafting_skill(CraftingSkills.ALCHEMY, 1)
                self.change_secondary_skill(SecondarySkills.ENGINEERING, 1)
            case Classes.PENITENT:
                attributes[Attributes.ENDURANCE] += 1
                attributes[Attributes.RESILIENCE] += 1
                combat_skills[CombatSkills.DEFENCE] += 13
                self.change_crafting_skill(CraftingSkills.ALCHEMY, 1)
                self.change_secondary_skill(SecondarySkills.MEDICINE, 1)

    def _get_initial_abilities(self) -> list:
        match self.get_char_class():
            case Classes.MARAUDER:
                return list(random.sample(list(Marauder), ABILITY_SLOT))
            case Classes.SENTINEL:
                return list(random.sample(list(Sentinel), ABILITY_SLOT))
            case Classes.STALKER:
                return list(random.sample(list(Stalker), ABILITY_SLOT))
            case Classes.TEMPLAR:
                return list(random.sample(list(Templar), ABILITY_SLOT))
            case Classes.PRIMALIST:
                return list(random.sample(list(Primalist), ABILITY_SLOT))
            case Classes.OCCULTIST:
                return list(random.sample(list(Occultist), ABILITY_SLOT))
            case Classes.CENOBITE:
                return list(random.sample(list(Cenobite), ABILITY_SLOT))
            case Classes.PENITENT:
                return list(random.sample(list(Penitent), ABILITY_SLOT))

    def _get_initial_gear(self):
        starting_gear = Equipment.get_starting_gear(self._char_class)
        for gear_key, gear_item in starting_gear.items():
            if gear_key == ItemType.RING:
                self.equip_gear(gear_item["left"], "left")
                self.equip_gear(gear_item["right"], "right")
            else:
                self.equip_gear(gear_item)

    def to_json(self):
        crafting_skills_data = {}
        for c in self.get_all_crafting_skills():
            crafting_skills_data[c.name] = self.get_crafting_skill(c)

        enhanced_crafting_skills_data = {}
        for ec in self.get_all_enhanced_crafting_skills():
            enhanced_crafting_skills_data[ec.name] = self.get_ehanced_crafting_skill(ec)

        secondary_skills_data = {}
        for s in self.get_all_secondary_skills():
            secondary_skills_data[s.name] = self.get_secondary_skill(s)

        enhanced_secondary_skills_data = {}
        for es in self.get_all_enhanced_secondary_skill():
            enhanced_secondary_skills_data[es.name] = self.get_enhanced_secondary_skill(
                es
            )
        gear_data = {}
        for slot, _ in self.get_all_equipment().items():
            if slot == ItemType.RING:
                gear_data[slot.name] = {}
                gear_data[slot.name]["left"] = self.get_equipement(
                    slot, "left"
                ).to_json()
                gear_data[slot.name]["right"] = self.get_equipement(
                    slot, "right"
                ).to_json()
            else:
                gear_data[slot.name] = self.get_equipement(slot).to_json()

        char_data = {
            "ancestry": self.get_ancestry().name.upper(),
            "class": self.get_char_class().name.upper(),
            "crafting_skills": crafting_skills_data,
            "enhanced_crafting_skills": enhanced_crafting_skills_data,
            "secondary_skills": secondary_skills_data,
            "enhanced_secondary_skills": enhanced_secondary_skills_data,
            "equipment": gear_data,
        }
        return {**super().to_json(), **char_data}

    # Nothing but getters and setters below this line

    # _crafting_skills
    def get_crafting_skill(self, skill: CraftingSkills) -> int:
        return self._crafting_skills[skill]

    def get_all_crafting_skills(self) -> dict:
        return self._crafting_skills

    def set_crafting_skill(self, skill: CraftingSkills, value: int):
        self._crafting_skills[skill] = value

    def change_crafting_skill(self, skill: CraftingSkills, change: int):
        self._crafting_skills[skill] += change

    # _enhanced_crafting_skills
    def get_ehanced_crafting_skill(self, skill: CraftingSkills) -> int:
        return self._enhanced_crafting_skills[skill]

    def get_all_enhanced_crafting_skills(self) -> dict:
        return self._enhanced_crafting_skills

    def set_enhanced_crafting_skill(self, skill: CraftingSkills, value: int):
        self._enhanced_crafting_skills[skill] = value

    def change_enhanced_crafting_skill(self, skill: CraftingSkills, change: int):
        self._enhanced_crafting_skills[skill] += change

    # _secondary_skills
    def get_secondary_skill(self, skill: SecondarySkills) -> int:
        return self._secondary_skills[skill]

    def get_all_secondary_skills(self) -> dict:
        return self._secondary_skills

    def set_secondary_skill(self, skill: SecondarySkills, value: int):
        self._secondary_skills[skill] = value

    def change_secondary_skill(self, skill: SecondarySkills, change: int):
        self._secondary_skills[skill] += change

    # _enhanced_secondary_skills
    def get_enhanced_secondary_skill(self, skill: SecondarySkills) -> int:
        return self._enhanced_secondary_skills[skill]

    def get_all_enhanced_secondary_skill(self) -> dict:
        return self._enhanced_secondary_skills

    def set_enhanced_secondary_skill(self, skill: SecondarySkills, value: int):
        self._enhanced_secondary_skills[skill] = value

    def change_enhanced_secondary_skill(self, skill: SecondarySkills, change: int):
        self._enhanced_secondary_skills[skill] += change

    # _ancestry
    def get_ancestry(self) -> Ancestry:
        return self._ancestry

    def set_ancestry(self, ancestry: Ancestry):
        self._ancestry = ancestry

    # _char_class
    def get_char_class(self) -> Classes:
        return self._char_class

    def set_char_class(self, char_class: Classes):
        self._char_class = char_class

    # _equipment
    def get_equipement(self, slot: ItemType, side=None) -> Equipment:
        if side is not None and slot == ItemType.RING:
            return self._equipment[slot][side]
        elif side is None and slot != ItemType.RING:
            return self._equipment[slot]
        else:
            raise ValueError(
                f"Misusing get equipment! {slot} is incompatible with {side}!"
            )

    def get_all_equipment(self) -> dict:
        return self._equipment

    def equip_gear(self, gear: Equipment, side=None):
        slot = gear.get_type()
        if side is not None and slot == ItemType.RING:
            if self._equipment[slot][side] is not None:
                self.unequip_gear(slot, side)
            self._equipment[slot][side] = gear
            self._equipment[slot][side].on_equip(self)
        elif side is None and slot != ItemType.RING:
            if self._equipment[slot] is not None:
                self.unequip_gear(slot)
            self._equipment[slot] = gear
            self._equipment[slot].on_equip(self)
        else:
            raise ValueError(
                f"Misusing equip gear! {slot} is incompatible with {side} for {gear.get_name()}!"
            )

    def unequip_gear(self, slot: ItemType, side=None):
        if self._equipment[slot] is not None:
            if side is not None:
                self._equipment[slot][side].on_unequip(self)
                self._equipment[slot][side] = None
            else:
                self._equipment[slot].on_unequip(self)
                self._equipment[slot] = None

    def clear_gear(self):
        self._equipment.clear()
