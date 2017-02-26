from crispy.ecs import System
from corerules import attacks, damages
import gui


universe = System()
world = universe.Entity()
dungeon = universe.Entity(world_x=0, world_y=0)
block1 = universe.Entity(x=50, y=200)
block2 = universe.Entity(x=100, y=50)
world.contents = list()
dungeon.contents = list()
world.contents.append(dungeon)
dungeon.contents.append(block1)
dungeon.contents.append(block2)


game = gui.GameApp(world)
game.run()


world = System()

player = universe.Entity(melee=5, ranged=0, max_hp=10, hp=10)
monster = universe.Entity(armor_class=2, max_hp=10, hp=10, resistances=["piercing"], vulnerabilities=["fire"])
bow = universe.Entity(ranged_bonus=3, ranged_damage=[1, 4])
arrow = universe.Entity(ranged_bonus=3, ranged_damage=["piercing", 10])
dagger = universe.Entity(melee_bonus=1, melee_damage=[1, 6])


def sneakattack(attack):
    if attack.check.vantage > 0:
        attack.dicepool.add_die(["piercing", 10])


def always_advantage(attack):
    attack.check.vantage += 1


def vulnerability_and_resistance(damage):
    for v in damage.target.vulnerabilities:
        if v in damage.roll:
            damage.roll[v] *= 2
    for r in damage.target.resistances:
        if r in damage.roll:
            damage.roll[r] //= 2


attacks.Attack.add_pre_rule(always_advantage)
damages.Damage.add_post_rule(vulnerability_and_resistance)

player.behaviors = dict()
player.behaviors["Attack"] = dict()
player.behaviors["Attack"]["attacker"] = [sneakattack]

result = attacks.Shoot(attacker=player, weapon=bow, ammo=arrow, target=monster)


print()
print()
print()
print("Attack")
print("Rolled: {}".format(result.check.roll))
print("({0}/{1}/{2})".format(result.check._first, result.check._low, result.check._high))
print("Bonus:  {}".format(result.check.bonus))
print("Total:  {}".format(result.check.get_total()))
print("DC:     {}".format(result.check.dc))
print()
print("HP:  {0}/{1}".format(monster.hp, monster.max_hp))
print()
print("Dice:   {}".format(result.dicepool))
