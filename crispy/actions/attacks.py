from . import core
from .damages import TakeDamage
from rolls import CheckType
from rolls import DamageType


melee_check = CheckType(["attacker.melee", "weapon.melee_bonus"], ["target.armor_class"])
melee_damage = DamageType(["weapon.melee_damage"])

range_check = CheckType(["attacker.ranged", "weapon.range_bonus"], ["target.armor_class"])
range_damage = DamageType(["weapon.ranged_damage"])


class AttackHit(core.Action):
    subjects = ("attacker", "weapon", "target")

    def __init__(self, damage_roll, *args):
        super().__init__(*args)
        self.damage_roll = damage_roll

    def after(self):
        super().after()
        TakeDamage(self.damage_roll.get(), self.target)


class AttackCritical(AttackHit):
    pass


class AttackMiss(core.Action):
    subjects = ("attacker", "weapon", "target")


class AttackFumble(AttackMiss):
    pass


class Attack(core.Action):
    subjects = ("attacker", "weapon", "target")
    cost = 5


class Melee(Attack):
    def __init__(self, *args):
        super().__init__(*args)
        self.check_roll = melee_check(self.get_subjects())
        self.damage_roll = melee_damage(self.get_subjects())

    class MeleeHit(AttackHit):
        pass

    class MeleeCrit(MeleeHit, AttackCritical):
        pass

    class MeleeMiss(AttackMiss):
        pass

    class MeleeFumble(MeleeMiss, AttackFumble):
        pass

    def after(self):
        super().after()
        if self.check_roll.is_critical():
            self.MeleeCrit(self.damage_roll, self.attacker, self.weapon, self.target)
        elif self.check_roll.is_success():
            self.MeleeHit(self.damage_roll, self.attacker, self.weapon, self.target)
        elif self.check_roll.is_fumble():
            self.MeleeFumble(self.attacker, self.weapon, self.target)
        else:
            self.MeleeMiss(self.attacker, self.weapon, self.target)


class Ranged(Attack):

    def __init__(self, *args):
        super().__init__(*args)
        self.check_roll = range_check(self.get_subjects())
        self.damage_roll = range_damage(self.get_subjects())

    class RangedHit(AttackHit):
        pass

    class RangedCrit(RangedHit, AttackCritical):
        pass

    class RangedMiss(AttackMiss):
        pass

    class RangedFumble(RangedMiss, AttackFumble):
        pass

    def after(self):
        super().after()
        if self.check_roll.is_critical():
            self.RangedCrit(self.damage_roll, self.attacker, self.weapon, self.target)
        elif self.check_roll.is_success():
            self.RangedHit(self.damage_roll, self.attacker, self.weapon, self.target)
        elif self.check_roll.is_fumble():
            self.RangedFumble(self.attacker, self.weapon, self.target)
        else:
            self.RangedMiss(self.attacker, self.weapon, self.target)

