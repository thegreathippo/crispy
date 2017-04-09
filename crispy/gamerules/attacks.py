from . import actions
from .checkrolls import CheckType
from .damagerolls import DamageType


@actions.abstract
class AttackHit(actions.Action):
    damage = None
    subjects = ["attacker", "weapon", "target"]

    def after(self):
        damage = self.damage.get()
        target = self.subjects[2]
        for v in damage.values():
            target.damage += v


@actions.abstract
class AttackCritical(AttackHit):
    pass


@actions.abstract
class AttackMiss(actions.Action):
    subjects = ["attacker", "weapon", "target"]


@actions.abstract
class AttackFumble(AttackMiss):
    pass


@actions.abstract
class Attack(actions.Action):
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

