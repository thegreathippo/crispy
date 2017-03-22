import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from gui.tilemaps import FloorMap, WallMap, Floor, Wall
from config import *
from kivy.lang import Builder
Builder.load_file('gui/game.kv')


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

kivy.require("1.9.0")


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.view = View()
        self.floormap = FloorMap(world, size_hint=(None, None))
        self.wallmap = WallMap(world, size_hint=(None, None))
        self.view.add_widget(self.floormap, 3)
        self.view.add_widget(self.wallmap, 2)
        world["tile"].on_new = self.add_tile
        world["tile"].on_del = self.remove_tile
        world["sprite"].on_new = self.add_sprite
        world["sprite"].on_del = self.remove_sprite

    def build(self):
        return self.view

    def add_tile(self, eid, pos):
        x, y, z = int(pos[0] * TILE_SIZE), int(pos[1] * TILE_SIZE), pos[2]
        params = {
            "size_hint": (None, None),
            "size": SPRITE_SIZE
        }
        if z == 0:
            params.update({
                "source": "gui/blocks/granite_floor.png",
                "pos": (x, y - (TILE_SIZE / 2))
            })
            floor = Floor(**params)
            self.floormap.add_tile(floor, eid, y)
        else:
            params.update({
                "source": "gui/blocks/granite_wall.png",
                "pos": (x, y)
            })
            wall = Wall(**params)
            self.wallmap.add_tile(wall, eid, y)

    def remove_tile(self, eid):
        if eid in self.floormap.tile_eid:
            self.floormap.remove_tile(eid)
        else:
            self.wallmap.remove_tile(eid)

    def add_sprite(self, eid, pos):
        pass

    def remove_sprite(self, eid):
        pass


class View(FloatLayout):

    def __init__(self):
        super().__init__()
        self.mode = None

    def erase_mode(self):
        self.mode = ERASE_MODE

    def draw_wall_mode(self):
        self.mode = DRAW_WALL_MODE

    def draw_floor_mode(self):
        self.mode = DRAW_FLOOR_MODE

