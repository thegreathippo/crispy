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

moves = [
    (1, 0),
    (0, 1),
    (1, 1),
    (-1, 0),
    (0, -1),
    (-1, -1),
    (1, -1),
    (-1, 1)
]

def expend_turn(entity):
    if entity == world.turn and entity != world.focus:
        vx, vy = random.choice(moves)
        world.move_block(entity, vx, vy, 0)
        print("{0} moved {1}, {2}".format(entity.eid, vx, vy))


world.register_process(gain_initiative, "initiative")
world.register_process(expend_turn, "initiative", priority=1)

app.run()
