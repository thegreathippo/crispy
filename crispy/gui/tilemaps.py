from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from config import *


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
        if touch.button == "left" and self.parent.mode in DRAW_MODE:
            if self.parent.mode == DRAW_FLOOR_MODE:
                z = 0
            else:
                z = 1
            x, y = int(touch.pos[0] // TILE_SIZE), int(touch.pos[1] // TILE_SIZE)
            try:
                self.world.set_block(x, y, z)
            except ValueError:
                pass
        for child in self.children:
            child.on_touch_down(touch)


class FloorMap(TileMap):
    pass

class WallMap(TileMap):
    pass


class Tile(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            eid = self.parent.tile_eid[self]
            if self.parent.parent.mode == ERASE_MODE:
                del self.parent.world["cell"][eid]
                del self.parent.world["tile"][eid]


class Floor(Tile):
    pass


class Wall(Tile):
    pass
