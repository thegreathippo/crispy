from .actions import EventAttack
from .damages import WeaponDamage, MeleeDamage, RangedDamage


class Attack(EventAttack):
    subjects = ["attacker", "weapon", "target"]
    damage_type = WeaponDamage

    def on_success(self):
        self.damage_type(self.dicepool, target=self.target)


class Melee(Attack):
    bonus = {"weapon": "melee_bonus",
             "attacker": "melee"}
    die = {"weapon": "melee_damage"}
    damage_type = MeleeDamage


class Ranged(Attack):
    bonus = {"weapon": "ranged_bonus",
             "attacker": "ranged"}
    die = {"weapon": "ranged_damage"}
    damage_type = RangedDamage


class Throw(Ranged):
    pass


class Shoot(Ranged):
    subjects = ["attacker", "weapon", "ammo", "target"]
    bonus = {"weapon": "ranged_bonus",
             "attacker": "ranged"}
    die = {"ammo": "ranged_damage"}
