from crispy.ecs import System
from corerules import attacks, damages
import gui
import worlds


world = worlds.World()

room = world.get_block(5, 5, 10, 10)
world.carve(room)

room = world.get_block(7, 7, 5, 3)
world.fill(room)

game = gui.GameApp(world)
game.run()
