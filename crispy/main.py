from game import world
import gui

app = gui.GameApp(world)


def gain_initiative(entity):
    pass
#    entity.initiative += 1
#    if entity.initiative > 0:
#        print("{}'s turn!".format(entity.eid))
#        world.turn = entity


world.register_process(gain_initiative, "initiative")


app.run()
