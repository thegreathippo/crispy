from game import world
import gui


app = gui.GameApp(world)

blocks = [
    (5, 5, 0),
    (5, 6, 0),
    (5, 7, 0),
    (6, 5, 0),
    (6, 6, 0),
    (6, 7, 0)
]


world.fill(*blocks)
app.run()
