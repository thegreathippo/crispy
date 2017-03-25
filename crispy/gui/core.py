import gui.layers
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import config


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

kivy.require("1.9.0")


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.mode = None

    def build(self):
        window = Window(self.world)
        return window

    def clicked_view(self, touch):
        x, y = config.transform_to_grid(*touch.pos)
        if self.mode is config.DRAW_ROOF_MODE:
            self.world.set_block(x, y, 2, image=config.IMG_GRANITE)
        elif self.mode is config.DRAW_WALL_MODE:
            self.world.set_block(x, y, 1, image=config.IMG_GRANITE)
        elif self.mode is config.DRAW_FLOOR_MODE:
            self.world.set_block(x, y, 0, image=config.IMG_GRANITE)
        elif self.mode is config.DRAW_PLAYER_MODE:
            self.world.set_block(x, y, 1, image=config.IMG_PLAYER)
        elif self.mode is config.DRAW_MONSTER_MODE:
            self.world.set_block(x, y, 1, image=config.IMG_MONSTER)
        elif self.mode is config.ERASE_MODE:
            block = self.world.get_block(x, y, 2)
            if block is None:
                block = self.world.get_block(x, y, 1)
            if block is None:
                block = self.world.get_block(x, y, 0)
            if block:
                self.world.del_block(block)


class Window(FloatLayout):

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self._world = world
        world["sprite"].on_new = self.load_sprite
        world["sprite"].on_del = self.remove_sprite

    def load_sprite(self, eid, pos):
        entity = self._world.get_entity(eid)
        self.ids["view_screen"].load_sprite(entity)

    def remove_sprite(self, eid):
        self.ids["view_screen"].remove_sprite(eid)

    def on_touch_down(self, touch):
        for child in self.children:
            if child.collide_point(*touch.pos):
                child.on_touch_down(touch)
                break
