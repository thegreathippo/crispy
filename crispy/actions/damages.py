from . import core


class TakeDamage(core.Action):

    def __init__(self, damage, *args):
        self.damage = damage
        super().__init__(*args)


class Croak(core.Action):
    pass

