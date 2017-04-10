from . import core


class TakeDamage(core.Action):
    subjects = ["agent"]

    def __init__(self, damage, *args, **kwargs):
        self.damage = damage
        super().__init__(*args, **kwargs)


