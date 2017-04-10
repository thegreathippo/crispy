import actions
from ecs.customdicts import CollisionError
from .core import world


class ActionBinding:
    def __init__(self):
        actions.movement.Step.bind_after(self.on_step)
        actions.attacks.Attack.bind_after(self.on_attack)
        actions.attacks.AttackHit.bind_after(self.on_attack_hit)
        actions.attacks.AttackMiss.bind_after(self.on_attack_miss)
        actions.attacks.AttackCritical.bind_after(self.on_attack_critical)
        actions.attacks.AttackFumble.bind_after(self.on_attack_fumble)

    @staticmethod
    def on_step(step):
        entity = step.subjects[0]
        x, y, z = entity.cell
        vx, vy, vz = step.direction
        pos = x + vx, y + vy, z + vz
        try:
            entity.cell = pos
            entity.sprite = pos[0], pos[1], pos[2], entity.sprite[3]
        except CollisionError as e:
            step.cost = 0   # we didn't take a step, so there's no cost
            target = world.Entity(e.blocking_key)
            if hasattr(target, "damage") and hasattr(entity, "energy"):
                sword = world.Entity(melee_damage=["slashing", 1, 6], melee_bonus=1, name="sword")
                actions.attacks.Melee(entity, sword, target)

    @staticmethod
    def on_attack(attack):
        attacker, weapon, target = attack.subjects
        text = "{0} attacked {1} with a {2}!".format(attacker.name, target.name, weapon.name)
        world.console.add(text)

    @staticmethod
    def on_attack_hit(hit):
        attacker, weapon, target = hit.subjects
        damage = hit.damage.get()
        text = "{0} hit {1} for {2} damage!".format(attacker.name, target.name, damage.total())
        world.console.add(text)

    @staticmethod
    def on_attack_miss(miss):
        attacker, weapon, target = miss.subjects
        text = "{0} missed {1}!".format(attacker.name, target.name)
        world.console.add(text)

    @staticmethod
    def on_attack_critical(critical):
        attacker, weapon, target = critical.subjects
        text = "{0} was critically hit!".format(target.name)
        world.console.add(text)

    @staticmethod
    def on_attack_fumble(fumble):
        attacker, weapon, target = fumble.subjects
        text = "{0} fumbled!".format(attacker.name)
        world.console.add(text)
