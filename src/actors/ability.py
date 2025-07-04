class Ability:
    def __init__(self, name: str, is_active: bool, has_target: bool, func, pref_targ):
        self.name = name
        self.is_active = is_active
        self.has_target = has_target
        self.func = func
        self.priority = 1
        self.pref_targ = pref_targ

    def execute(self, source, target):
        if self.has_target:
            # Will need to get target by using pref_targ
            self.func(source, target)
        else:
            self.func(source)
