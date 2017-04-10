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


class ClearEntity:
    eids = list()

    @staticmethod
    def run(entity):
        ClearEntity.eids.append(entity.eid)

    @staticmethod
    def clear():
        for eid in ClearEntity.eids:
            entity = world.Entity(eid)
            world.clear(entity)
        ClearEntity.eids.clear()


def clear_entity(entity):
    world.clear(entity)


world.register_process(gain_energy, domain="energy")
world.register_process(take_action, domain="energy")
world.register_process(clear_entity, domain="dead")

app.run()

