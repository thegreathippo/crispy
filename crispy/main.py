import random
import game
import actions
import constants
import gui

world = game.world
app = gui.app


def gain_energy(entity):
    if entity.energy < 0:
        entity.energy += 1

directions = list(constants.DIRECTIONS.values())


def take_action(entity):
    if entity.energy >= 0 and entity != world.focus:
        direction = random.choice(directions)
        actions.movement.steps[direction](entity)


def clear_entity(entity):
    world.clear_entity(entity)


world.processes.register(gain_energy, domain="energy")
world.processes.register(take_action, domain="energy")
world.processes.register(clear_entity, domain="dead")

app.run()

