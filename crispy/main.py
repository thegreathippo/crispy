from world import game
import gui


app = gui.GameApp(game)

game.fill(5, 5, 0)
game.fill(4, 4, 0)
game.fill(3, 3, 0)
game.fill(2, 2, 0)
game.fill(1, 1, 0)
app.run()
