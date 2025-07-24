import random

from src.game_types import (
    Attributes,
    CombatSkills,
    CraftingSkills,
    SecondarySkills,
    ItemType,
)

from src.equipment.t0gear import T0Gear

from src.actors.characters.classes.classes import Classes


class Equipment:
    def __init__(self, gear_info: dict):
        self._name = gear_info["name"]
        if isinstance(gear_info["type"], str):
            self._type = ItemType[gear_info["type"]]
        else:
            self._type = gear_info["type"]

        stat = gear_info["stat"]
        if isinstance(stat, str):
            if stat in list(Attributes.__members__.keys()):
                self._stat = Attributes[stat]
            elif stat in list(CombatSkills.__members__.keys()):
                self._stat = CombatSkills[stat]
            elif stat in list(CraftingSkills.__members__.keys()):
                self._stat = CraftingSkills[stat]
            elif stat in list(SecondarySkills.__members__.keys()):
                self._stat = SecondarySkills[stat]
            else:
                self._stat = stat
        else:
            self._stat = stat

        self._value = gear_info["value"]
        self._effect = callable
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
        char_classes = []
        class_data = gear_info["class"]
        for c in class_data:
            if isinstance(c, str):
                char_classes.append(Classes[c])
            else:
                char_classes.append(c)
        self._class = char_classes

        self._recipe = gear_info["recipe"]
        if isinstance(gear_info["craft"], str):
            self._craft = CraftingSkills[gear_info["craft"]]
        else:
            self._craft = gear_info["craft"]

        self._sell = gear_info["sell"]

        if isinstance(self._stat, list):
            self._effect(self)

    @classmethod
    def get_starting_gear(cls, char_class: Classes) -> dict:
        match char_class:
            case Classes.MARAUDER:
                return {
                    ItemType.HELMET: Equipment(T0Gear.LEAD_CAP.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.LEAD_DISK.value),
                    ItemType.GLOVES: Equipment(T0Gear.LEAD_KNUCKLES.value),
                    ItemType.BOOTS: Equipment(T0Gear.LEAD_GRIEVES.value),
                    ItemType.WEAPON: Equipment(
                        random.choice(
                            [T0Gear.RUSTY_MAUL.value, T0Gear.RUSTY_GREATAXE.value]
                        )
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.SENTINEL:
                return {
                    ItemType.HELMET: Equipment(T0Gear.BONE_MASK.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.BONE_VEST.value),
                    ItemType.GLOVES: Equipment(T0Gear.BONE_GLOVES.value),
                    ItemType.BOOTS: Equipment(T0Gear.BONE_GRIEVES.value),
                    ItemType.WEAPON: Equipment(
                        random.choice(
                            [
                                T0Gear.RUSTY_LONGSWORD.value,
                                T0Gear.RUSTY_TWIN_DAGGERS.value,
                            ]
                        )
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.STALKER:
                return {
                    ItemType.HELMET: Equipment(T0Gear.BONE_MASK.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.BONE_VEST.value),
                    ItemType.GLOVES: Equipment(T0Gear.BONE_VAMBRACES.value),
                    ItemType.BOOTS: Equipment(T0Gear.BONE_GRIEVES.value),
                    ItemType.WEAPON: Equipment(
                        random.choice(
                            [T0Gear.OLD_SHORTBOW.value, T0Gear.OLD_LONGBOW.value]
                        )
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.TEMPLAR:
                return {
                    ItemType.HELMET: Equipment(T0Gear.LINEN_VEIL.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.LINEN_VESTMENTS.value),
                    ItemType.GLOVES: Equipment(T0Gear.LINEN_WRAPS.value),
                    ItemType.BOOTS: Equipment(T0Gear.STRAW_SANDALS.value),
                    ItemType.WEAPON: Equipment(
                        random.choice(
                            [
                                T0Gear.RUSTY_MAUL.value,
                                T0Gear.RUSTY_MACE_AND_SHIELD.value,
                            ]
                        )
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.PRIMALIST:
                return {
                    ItemType.HELMET: Equipment(T0Gear.BONE_MASK.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.BONE_VEST.value),
                    ItemType.GLOVES: Equipment(T0Gear.BONE_BRACELETS.value),
                    ItemType.BOOTS: Equipment(T0Gear.BONE_GRIEVES.value),
                    ItemType.WEAPON: Equipment(
                        random.choice(
                            [T0Gear.DUSTY_ROD.value, T0Gear.DUSTY_RITUAL_DAGGER.value]
                        )
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.OCCULTIST:
                return {
                    ItemType.HELMET: Equipment(T0Gear.LINEN_VEIL.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.LINEN_VESTMENTS.value),
                    ItemType.GLOVES: Equipment(T0Gear.LINEN_GLOVES.value),
                    ItemType.BOOTS: Equipment(T0Gear.STRAW_SANDALS.value),
                    ItemType.WEAPON: Equipment(
                        random.choice([T0Gear.DUSTY_TOME.value, T0Gear.DUSTY_ORB.value])
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.CENOBITE:
                return {
                    ItemType.HELMET: Equipment(T0Gear.LINEN_VEIL.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.LINEN_VESTMENTS.value),
                    ItemType.GLOVES: Equipment(T0Gear.LINEN_GLOVES.value),
                    ItemType.BOOTS: Equipment(T0Gear.STRAW_SANDALS.value),
                    ItemType.WEAPON: Equipment(
                        random.choice([T0Gear.OLD_STAFF.value, T0Gear.OLD_WHIP.value])
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }
            case Classes.PENITENT:
                return {
                    ItemType.HELMET: Equipment(T0Gear.LEAD_CAP.value),
                    ItemType.CHESTPIECE: Equipment(T0Gear.LEAD_DISK.value),
                    ItemType.GLOVES: Equipment(T0Gear.LEAD_VAMBRACES.value),
                    ItemType.BOOTS: Equipment(T0Gear.LEAD_GRIEVES.value),
                    ItemType.WEAPON: Equipment(
                        random.choice([T0Gear.OLD_WHIP.value, T0Gear.OLD_CLUB.value])
                    ),
                    ItemType.AMULET: Equipment(T0Gear.RAT_AMULET.value),
                    ItemType.RING: {
                        "left": Equipment(T0Gear.LEAD_RING.value),
                        "right": Equipment(T0Gear.LEAD_RING.value),
                    },
                }

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
        elif stat == "INITIATIVE":
            source.change_initiative_mod(self.get_value())
        elif stat == "ARMOUR":
            source.change_armour(self.get_value())
        elif stat is None:
            pass
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
            effect_data = self.get_name().lower()

        class_data = []
        for c in self.get_class():
            class_data.append(c.name.upper())

        stat_data = self.get_stat()
        if stat_data is not None and not isinstance(stat_data, str):
            stat_data = stat_data.name.upper()

        return {
            "name": self.get_name(),
            "type": self.get_type().name.upper(),
            "stat": stat_data,
            "value": self.get_value(),
            "effect": effect_data,
            "tier": self.get_tier(),
            "class": class_data,
            "recipe": self.get_recipe(),
            "craft": self.get_craft().name.upper(),
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
