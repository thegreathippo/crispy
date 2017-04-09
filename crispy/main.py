import random
import worlds
import gamerules
import constants
import gui

world = worlds.world
app = gui.app


def gain_energy(entity):
    if entity.energy < 0:
        entity.energy += 1

directions = list(constants.DIRECTIONS.values())

sword = world.Entity(melee_bonus=1, melee_damage=["slashing", 1, 6])


def take_action(entity):
    if entity.energy >= 0 and entity != world.focus:
        direction = random.choice(directions)
        try:
            gamerules.movement.steps[direction](entity)
        except ValueError as e:
            target = world.Entity(e.blocking_key)
            if hasattr(target, "damage"):
                melee = gamerules.attacks.Melee(entity, sword, target)
                app.add_to_console(melee.check)

world.register_process(gain_energy, domain="energy")
world.register_process(take_action, domain="energy")

app.run()

