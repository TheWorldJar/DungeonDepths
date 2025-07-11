from enum import Enum

from src.actors.status import Status


class PrefTarget(Enum):
    """
    The valid prefered targets for abilities.
    FIRST & LAST refer to initiative positions.
    LOW & HIGH refer to current health of a potential target.
    SELF & ALL are included for clarity.
    """

    FIRST = "first"
    LAST = "last"
    NOT_FIRST = "not_first"
    NOT_LAST = "not_last"
    ANY = "any"
    LOW = "low"
    HIGH = "high"
    ALL = "all"
    SELF = "self"


class Ability:
    def __init__(
        self,
        name: str,
        is_active: bool,
        has_target: bool,
        func,
        pref_targ: PrefTarget,
        duration: float | int,
    ):
        self.name = name
        self.is_active = is_active
        self.has_target = has_target
        self.func = func
        self.priority = 1
        self.pref_targ = pref_targ
        self.duration = duration

    def execute(self, source, target):
        if self.has_target:
            # Will need to get target by using pref_targ
            self.func(source, target)
        else:
            self.func(source)

    def apply(self, source):
        source.add_effect(Status(self.name, self.func, self.duration))
