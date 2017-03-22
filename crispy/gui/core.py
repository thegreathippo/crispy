import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

kivy.require("1.9.0")

TILE_SIZE = 16
SPRITE_SIZE = TILE_SIZE, TILE_SIZE + (TILE_SIZE // 2)


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.view = FloatLayout()
        self.floormap = TileMap(world, size=(900, 900), size_hint=(None, None))
        self.wallmap = TileMap(world, size=(900, 900), size_hint=(None, None))
        self.view.add_widget(self.floormap)
        self.view.add_widget(self.wallmap)
        world["tile"].on_new = self.add_tile
        world["tile"].on_del = self.remove_tile

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
                "source": "gui/granite_floor.png",
                "pos": (x, y - (TILE_SIZE / 2))
            })
            floor = Floor(**params)
            self.floormap.add_tile(floor, eid, y)
        else:
            params.update({
                "source": "gui/granite_wall.png",
                "pos": (x, y)
            })
            wall = Wall(**params)
            self.wallmap.add_tile(wall, eid, y)

    def remove_tile(self, eid):
        if eid in self.floormap.tile_eid:
            self.floormap.remove_tile(eid)
        else:
            self.wallmap.remove_tile(eid)


class TileMap(FloatLayout):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.y_map = dict()
        self.tile_eid = dict()

    def add_tile(self, tile, eid, y=0):
        self.y_map[tile] = y
        self.tile_eid[tile] = eid
        self.tile_eid[eid] = tile
        self.refresh()

    def remove_tile(self, eid):
        tile = self.tile_eid[eid]
        del self.tile_eid[tile]
        del self.tile_eid[eid]
        del self.y_map[tile]
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        tiles = [t for t in self.y_map.keys()]
        tiles = sorted(tiles, key=lambda t: self.y_map[t], reverse=True)
        for tile in tiles:
            self.add_widget(tile)

    def on_touch_down(self, touch):
        if not touch.is_double_tap:
            if touch.button == "left":
                z = 0
            else:
                z = 1
            x, y = int(touch.pos[0] // TILE_SIZE), int(touch.pos[1] // TILE_SIZE)
            try:
                e = self.world.set_block(x, y, z)
            except ValueError:
                pass
        else:
            for child in self.children:
                child.on_touch_down(touch)


class Tile(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            eid = self.parent.tile_eid[self]
            del self.parent.world["cell"][eid]
            del self.parent.world["tile"][eid]


class Floor(Tile):
    pass


class Wall(Tile):
    pass

