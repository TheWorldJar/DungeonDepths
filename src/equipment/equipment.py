from enum import Enum

from src.actors.actor import CombatSkills, Attributes
from src.actors.characters.character import SecondarySkills, CraftingSkills

from src.equipment.t0gear import T0Gear


class ItemType(Enum):
    HELMET = "helmet"
    CHESTPIECE = "chestpiece"
    GLOVES = "gloves"
    BOOTS = "boots"
    WEAPON = "weapon"
    RING = "ring"
    AMULET = "amulet"


class Equipment:
    def __init__(self, gear_info: dict):
        self._name = gear_info["name"]
        self._type = ItemType[gear_info["type"]]
        self._stat = gear_info["stat"]
        self._value = gear_info["value"]
        if isinstance(gear_info["effect"], str):
            match gear_info["tier"]:
                case 0:
                    enum_member = T0Gear[gear_info["name"].upper()]
                case _:
                    raise ValueError("Equipment tier is too high!")
            self._effect = enum_member.value["effect"]
        else:
            self._effect = gear_info["effect"]
        self._tier = gear_info["tier"]
        self._class = gear_info["class"]
        self._recipe = gear_info["recipe"]
        self._craft = gear_info["craft"]
        self._sell = gear_info["sell"]

        if isinstance(self._stat, list):
            self._effect(self)

    def on_equip(self, source):
        stat = self.get_stat()
        if stat in Attributes:
            source.change_enhanced_attribute(stat, self.get_value())
        elif stat in CombatSkills:
            source.change_enhanced_combat_skill(stat, self.get_value())
        elif stat in SecondarySkills:
            source.change_enhanced_secondary_skill(stat, self.get_value())
        elif stat in CraftingSkills:
            source.change_enhanced_crafting_skill(stat, self.get_value())
        elif stat == "initiative":
            source.change_initiative_mod(self.get_value())
        elif stat == "armour":
            source.change_armour(self.get_value())
        else:
            raise ValueError(
                f"{source.get_name()}'s {self.get_name()}'s {stat} is invalid!"
            )

    def on_unequip(self, source):
        self.set_value(-(self.get_value()))
        self.on_equip(source)

    def to_json(self):
        effect_data = self.get_effect()
        if effect_data is not None:
            self.get_name().upper()
        return {
            "name": self.get_name(),
            "type": self.get_type().name,
            "stat": self.get_stat(),
            "value": self.get_value(),
            "effect": effect_data,
            "tier": self.get_tier(),
            "class": self.get_class(),
            "recipe": self.get_recipe(),
            "craft": self.get_craft(),
            "sell": self.get_sell(),
        }

    # Nothing but getters and setters below.
    # _name
    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    # _type
    def get_type(self) -> ItemType:
        return self._type

    def set_type(self, item_type: ItemType):
        self._type = item_type

    # _stat
    def get_stat(self):
        return self._stat

    def set_stat(self, stat):
        self._stat = stat

    # _value
    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int):
        self._value = value

    def change_value(self, change: int):
        self._value += change

    # _effect
    def get_effect(self):
        return self._effect

    def set_effect(self, effect):
        self._effect = effect

    # _tier
    def get_tier(self) -> int:
        return self._tier

    def set_tier(self, tier: int):
        self._tier = tier

    # _class
    def get_class(self):
        return self._class

    def set_class(self, char_class):
        self._class = char_class

    # _recipe
    def get_recipe(self):
        return self._recipe

    def set_recipe(self, recipe: dict):
        self._recipe = recipe

    # _craft
    def get_craft(self):
        return self._craft

    def set_craft(self, skill):
        self._craft = skill

    # _sell
    def get_sell(self) -> int:
        return self._sell

    def set_sell(self, sell: int):
        self._sell = sell
