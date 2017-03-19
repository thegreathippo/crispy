import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

kivy.require("1.9.0")

TILE_SIZE = 20


class GameApp(App):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.tilemap = TileMap(size=(900, 900), size_hint=(None, None))
        self.eid_to_tile = dict()
        game["tile_pos"].on_add(self.add_tile)

    def build(self):
        return self.tilemap

    def add_tile(self, eid, pos):
        xy = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        tile = Tile(pos=xy, size_hint=(None, None), size=(TILE_SIZE, TILE_SIZE))
        self.eid_to_tile[eid] = tile
        self.tilemap.add_widget(tile)


class TileMap(FloatLayout):
    pass


class Tile(Button):
    pass
