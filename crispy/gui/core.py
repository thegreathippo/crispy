from gui.views import View
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
Builder.load_file('gui/game.kv')


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

kivy.require("1.9.0")


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.view = View(world)
        world["tile"].on_new = self.view.add_tile
        world["tile"].on_del = self.view.remove_tile
        world["sprite"].on_new = self.add_sprite
        world["sprite"].on_del = self.remove_sprite

    def build(self):
        return self.view

    def add_sprite(self, eid, pos):
        pass

    def remove_sprite(self, eid):
        pass


