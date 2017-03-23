from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from config import *


class TileMap(FloatLayout):
    pass


class FloorMap(TileMap):
    pass


class WallMap(TileMap):
    pass


class BaseTile(Image):
    def __init__(self, z):
        super().__init__()
        self.allow_stretch = True
        self.size = SPRITE_SIZE
        self.size_hint = None, None
        self.z = z

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True


class Floor(BaseTile):
    def __init__(self, x, y, z):
        super().__init__(z)
        self.source = "gui/blocks/granite_floor.png"
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE - (TILE_SIZE // 2)


class Wall(BaseTile):
    def __init__(self, x, y, z):
        super().__init__(z)
        self.source = "gui/blocks/granite_wall.png"
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
