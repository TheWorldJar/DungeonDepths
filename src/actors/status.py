from src.const import NO_DURATION, END_DURATION


# Mostly Placeholder
class Status:
    def __init__(self, name: str, func, duration: float | int):
        self.name = name
        self.func = func
        self.duration = duration

    def execute(self, source):
        self.func(source)
        if self.duration < NO_DURATION:
            self.duration -= 1
            if self.duration <= 0:
                source.remove_effect(self)
