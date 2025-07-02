class Ability:
    def __init__(self, name: str, is_active: bool, func):
        self.name = name
        self.is_active = is_active
        self.func = func

    def execute(self, source, target):
        self.func(source, target)
