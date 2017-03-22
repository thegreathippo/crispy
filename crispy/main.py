from game import world
import gui


app = gui.GameApp(world)

blocks = [
    (5, 5, 0)
]


world.fill(*blocks)
app.run()
