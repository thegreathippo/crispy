from .actions import LocalEvent


class Damage(LocalEvent):
    subjects = ["target"]

    def __init__(self, dicepool, **kwargs):
        self.roll = dicepool.get_roll()

    def finalize(self):
        self.target.hp -= self.roll.get_total()


class WeaponDamage(Damage):
    pass


class MeleeDamage(WeaponDamage):
    pass


class RangedDamage(WeaponDamage):
    pass

