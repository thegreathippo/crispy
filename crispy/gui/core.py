import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


kivy.require("1.9.0")

TILE_SIZE = 0.05, 0.05


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.tilemap = TileMap(size=(900, 900), pos=(0, 0), size_hint=(None, None))

    def build(self):
        window = RootWindow()
        view = ViewWindow(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        view.add_widget(self.tilemap)
        menu = BottomMenu(size_hint=(.5, .15), pos_hint={"center_x": 0.5, "bottom": 0},
                          orientation="horizontal")
        window.add_widget(view)
        window.add_widget(menu)
        self.tilemap.load(self.world)
        return window


class RootWindow(FloatLayout):
    pass


class ViewWindow(ScrollView):
    pass


class TileMap(FloatLayout):

    def load(self, world):
        self.clear_widgets()
        for cell in world:
            img = "gui/" + cell.image + ".png"
            pos = cell.x * 32, cell.y * 32
            size = 31, 31
            size_hint = None, None
            tile = Tile(background_normal=img, size_hint=size_hint, size=size, pos=pos)
            self.add_widget(tile)


class Tile(Button):
    pass


class BottomMenu(BoxLayout):
    pass

