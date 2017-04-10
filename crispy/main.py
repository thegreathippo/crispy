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

sword = world.Entity(melee_bonus=1, melee_damage=["slashing", 1, 6])


def take_action(entity):
    if entity.energy >= 0 and entity != world.focus:
        direction = random.choice(directions)
        actions.movement.steps[direction](entity)

world.register_process(gain_energy, domain="energy")
world.register_process(take_action, domain="energy")

app.run()

