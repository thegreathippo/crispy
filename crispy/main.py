from game import world
import gui
import random

app = gui.GameApp(world)


def gain_initiative(entity):
    entity.initiative += 1
    if entity.initiative >= 0:
        world.turn = entity
    elif world.turn == entity:
        world.turn = world.null


def expend_turn(entity):
    if entity == world.turn and entity != world.focus:
        vx, vy = random.randint(-1, 1), random.randint(-1, 1)
        world.move_block(entity, vx, vy, 0)
        entity.initiative -= random.randint(5, 10)


world.register_process(gain_initiative, "initiative")
world.register_process(expend_turn, "initiative", priority=1)

app.run()
