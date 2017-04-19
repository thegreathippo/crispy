import actions
from customdicts import CollisionError
from .core import world


class ActionBinding:
    def __init__(self):
        actions.core.Action.bind_after(self.on_action)
        actions.movement.Step.bind_after(self.on_step)
        actions.attacks.Attack.bind_after(self.on_attack)
        actions.attacks.AttackHit.bind_after(self.on_attack_hit)
        actions.attacks.AttackMiss.bind_after(self.on_attack_miss)
        actions.attacks.AttackCritical.bind_after(self.on_attack_critical)
        actions.attacks.AttackFumble.bind_after(self.on_attack_fumble)
        actions.damages.TakeDamage.bind_after(self.on_take_damage)
        actions.damages.Croak.bind_after(self.on_croak)

    @staticmethod
    def on_step(step):
        entity = step.agent
        x, y, z = entity.cell
        vx, vy, vz = step.direction
        pos = x + vx, y + vy, z + vz
        try:
            entity.cell = pos
            entity.sprite = pos[0], pos[1], pos[2], entity.sprite[3]
        except CollisionError as e:
            step.cost = 0   # we didn't take a step, so there's no cost
            target = world.get_entity(e.blocking_key)
            if hasattr(target, "damage") and hasattr(entity, "energy"):
                sword = world.new_entity(melee_damage=["slashing", 1, 6], melee_bonus=1, name="sword")
                actions.attacks.Melee(entity, sword, target)

    @staticmethod
    def on_action(action):
        pass

    @staticmethod
    def on_attack(attack):
        attacker, weapon, target = attack.attacker, attack.weapon, attack.target
        text = "{0} attacked {1} with a {2}!".format(attacker.name, target.name, weapon.name)
        world.console.add(text)

    @staticmethod
    def on_attack_hit(hit):
        attacker = hit.attacker
        target = hit.target
        text = "{0} hit {1}!".format(attacker.name, target.name)
        world.console.add(text)

    @staticmethod
    def on_attack_miss(miss):
        attacker = miss.attacker
        target = miss.target
        text = "{0} missed {1}!".format(attacker.name, target.name)
        world.console.add(text)

    @staticmethod
    def on_attack_critical(critical):
        target = critical.target
        text = "{0} was critically hit!".format(target.name)
        world.console.add(text)

    @staticmethod
    def on_attack_fumble(fumble):
        attacker = fumble.attacker
        text = "{0} fumbled!".format(attacker.name)
        world.console.add(text)

    @staticmethod
    def on_take_damage(take_damage):
        agent = take_damage.agent
        damage = take_damage.damage
        agent.damage += damage.total()
        remaining_hp = agent.max_hp - agent.damage
        text = "{0} took {1} damage! (HP: {2})".format(agent.name, damage, remaining_hp)
        world.console.add(text)
        if agent.damage >= agent.max_hp:
            actions.damages.Croak(agent)

    @staticmethod
    def on_croak(croak):
        entity = croak.agent
        text = "{0} has croaked!".format(entity.name)
        world.console.add(text)
        world.clear_entity(entity)

