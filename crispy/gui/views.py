from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from gui.tilemaps import FloorMap, WallMap, Floor, Wall
from config import *


class TileData:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class EditButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = 50, 30


class View(FloatLayout):

    def __init__(self, world):

        super().__init__()
        self.world = world
        self.mode = None
        self.floormap = FloorMap(size_hint=(None, None))
        self.wallmap = WallMap(size_hint=(None, None))
        erase = EditButton(text="erase", x=0, on_press=self.button_click)
        wall = EditButton(text="wall", x=50, on_press=self.button_click)
        floor = EditButton(text="floor", x=100, on_press=self.button_click)
        save = EditButton(text="save", x=150, on_press=self.button_click)
        load = EditButton(text="load", x=200, on_press=self.button_click)
        clear = EditButton(text="clear", x=250, on_press=self.button_click)
        self.buttons = [erase, wall, floor, save, load, clear]
        self.add_widget(erase)
        self.add_widget(wall)
        self.add_widget(floor)
        self.add_widget(save)
        self.add_widget(load)
        self.add_widget(clear)
        self.add_widget(self.floormap, 3)
        self.add_widget(self.wallmap, 2)
        self.eid_to_tile = dict()
        self.tiles_by_depth = dict()

    def add_tile(self, eid, pos):
        tile = TileData(*pos)
        self.eid_to_tile[eid] = tile
        if tile.z not in self.tiles_by_depth:
            self.tiles_by_depth[tile.z] = list()
        self.tiles_by_depth[tile.z].append(tile)
        self.tiles_by_depth[tile.z].sort(key=lambda t: t.y, reverse=True)
        self.refresh()

    def remove_tile(self, eid):
        tile = self.eid_to_tile[eid]
        del self.eid_to_tile[eid]
        self.tiles_by_depth[tile.z].remove(tile)
        if not self.tiles_by_depth[tile.z]:
            del self.tiles_by_depth[tile.z]
        self.refresh()

    def refresh(self):
        self.floormap.clear_widgets()
        self.wallmap.clear_widgets()
        for tile in self.tiles_by_depth.get(0, list()):
            block = Floor(tile.x, tile.y, tile.z)
            self.floormap.add_widget(block)
        for tile in self.tiles_by_depth.get(1, list()):
            block = Wall(tile.x, tile.y, tile.z)
            self.wallmap.add_widget(block)

    def get_cell_pos(self, click_pos):
        x = int(click_pos[0] // TILE_SIZE)
        y = int(click_pos[1] // TILE_SIZE)
        return x, y

    def button_click(self, button):
        if button.text is "erase":
            self.mode = ERASE_MODE
        elif button.text is "wall":
            self.mode = DRAW_WALL_MODE
        elif button.text is "floor":
            self.mode = DRAW_FLOOR_MODE
        elif button.text is "save":
            self.world.save()
        elif button.text is "load":
            self.world.load()
        elif button.text is "clear":
            self.world.clear()

    def on_touch_down(self, touch):
        x, y = self.get_cell_pos(touch.pos)
        caught = False
        for child in self.children:
            if child.on_touch_down(touch):
                if child in self.buttons:
                    caught = True
        if not caught:
            if self.mode is DRAW_WALL_MODE:
                self.world.set_block(x, y, 1)
            elif self.mode is DRAW_FLOOR_MODE:
                self.world.set_block(x, y, 0)
            elif self.mode is ERASE_MODE:
                block = self.world.get_block(x, y, 1)
                if not block:
                    block = self.world.get_block(x, y, 0)
                if block:
                    del block.tile
                    del block.cell

