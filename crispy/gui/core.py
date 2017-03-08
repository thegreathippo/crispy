import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


kivy.require("1.9.0")

TILE_SIZE = 20


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.tilemap = TileMap(self.world, size=(900, 900), pos=(0, 0), size_hint=(None, None))

    def build(self):
        window = RootWindow()
        view = ViewWindow(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        view.add_widget(self.tilemap)
        menu = BottomMenu(size_hint=(.5, .15), pos_hint={"center_x": 0.5, "bottom": 0},
                          orientation="horizontal")
        window.add_widget(view)
        window.add_widget(menu)
        return window


class RootWindow(FloatLayout):
    pass


class ViewWindow(ScrollView):
    pass


class TileMap(FloatLayout):

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.load()

    def refresh(self, cell):
        self.remove_widget(cell.tile)
        self.load_tile(cell)

    def load_tile(self, cell):
        tile = Tile(cell)
        cell.tile = tile
        cell.gui_callback = self.refresh
        self.add_widget(tile)

    def load(self):
        self.clear_widgets()
        for cell in self.world:
            self.load_tile(cell)


class Tile(Button):
    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = TILE_SIZE - 1, TILE_SIZE - 1
        self.pos = cell.x * TILE_SIZE, cell.y * TILE_SIZE
        self.background_normal = "gui/" + cell.image + ".png"
        self.cell = cell

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.world.fill([self.cell])


class BottomMenu(BoxLayout):
    pass

