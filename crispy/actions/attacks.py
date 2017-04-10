from . import core
from .checkrolls import CheckType
from .damagerolls import DamageType


@core.abstract
class AttackHit(core.Action):
    damage = None
    subjects = ["attacker", "weapon", "target"]


@core.abstract
class AttackCritical(AttackHit):
    pass


@core.abstract
class AttackMiss(core.Action):
    subjects = ["attacker", "weapon", "target"]


@core.abstract
class AttackFumble(AttackMiss):
    pass


@core.abstract
class Attack(core.Action):
    subjects = ["attacker", "weapon", "target"]
    cost = 5


class Melee(Attack):
    check = CheckType(["attacker.melee", "weapon.melee_bonus"],
                      ["target.armor_class"])

    class MeleeHit(AttackHit):
        damage = DamageType(["weapon.melee_damage"])

    class MeleeCrit(MeleeHit, AttackCritical):
        pass

    class MeleeMiss(AttackMiss):
        pass

    class MeleeFumble(MeleeMiss, AttackFumble):
        pass

    def after(self):
        if self.check.is_critical():
            self.MeleeCrit(*self.subjects)
        elif self.check.is_success():
            self.MeleeHit(*self.subjects)
        elif self.check.is_fumble():
            self.MeleeFumble(*self.subjects)
        else:
            self.MeleeMiss(*self.subjects)


class Ranged(Attack):
    check = CheckType(["attacker.ranged", "weapon.ranged_bonus"],
                      ["target.armor_class"])

    class RangedHit(AttackHit):
        damage = DamageType(["weapon.melee_damage"])

    class RangedCrit(RangedHit, AttackCritical):
        pass

    class RangedMiss(AttackMiss):
        pass

    class RangedFumble(RangedMiss, AttackFumble):
        pass

    def after(self):
        if self.check.is_critical():
            self.RangedCrit(*self.subjects)
        elif self.check.is_success():
            self.RangedHit(*self.subjects)
        elif self.check.is_fumble():
            self.RangedFumble(*self.subjects)
        else:
            self.RangedMiss(*self.subjects)

