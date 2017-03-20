import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

kivy.require("1.9.0")

TILE_SIZE = 20


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.tilemap = TileMap(world, size=(900, 900), size_hint=(None, None))
        self.eid_to_tile = dict()
        world["tile_pos"].on_add(self.add_tile)
        world["tile_pos"].on_remove(self.remove_tile)

    def build(self):
        return self.tilemap

    def add_tile(self, eid, pos):
        xy = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        tile = Tile(pos=xy, size_hint=(None, None), size=(TILE_SIZE, TILE_SIZE))
        self.eid_to_tile[eid] = tile
        self.tilemap.add_widget(tile)

    def remove_tile(self, eid):
        tile = self.eid_to_tile[eid]
        self.tilemap.remove_widget(tile)


class TileMap(FloatLayout):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world

    def on_touch_down(self, touch):
        x, y = int(touch.pos[0] // TILE_SIZE), int(touch.pos[1] // TILE_SIZE)
        self.world.add_block(x, y, 0)


class Tile(Button):
    pass
