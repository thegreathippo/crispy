import constants
import random

from game import world
import gui
app = gui.GameApp(world)


def gain_energy(entity):
    if entity.energy < 0:
        entity.energy += 1

directions = list(constants.DIRECTIONS.values())


def take_action(entity):
    if entity.energy >= 0 and entity != world.focus:
        entity.energy -= 5
        direction = random.choice(directions)
        try:
            vx, vy, vz = direction
            x, y, z = vx + entity.x, vy + entity.y, vz + entity.z
            entity.cell = x, y, z
            entity.sprite = x, y, z, entity.sprite.image
        except ValueError:
            pass

world.register_process(gain_energy, domain="energy")
world.register_process(take_action, domain="energy")

app.run()

