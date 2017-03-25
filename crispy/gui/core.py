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

    def build(self):
        window = Window(self.world)
        return window

    def clicked_view(self, touch):
        pass


class Window(FloatLayout):

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        world["sprite"].on_new = self.load_sprite
        world["sprite"].on_del = self.remove_sprite
        world.camera.register(self.move_camera)
        self.mode = None

    def load_sprite(self, eid, pos):
        entity = self.world.get_entity(eid)
        self.ids["view_screen"].load_sprite(entity)

    def remove_sprite(self, eid):
        self.ids["view_screen"].remove_sprite(eid)

    def move_camera(self, old_pos, new_pos):
        self.ids["view_screen"].move_camera(old_pos, new_pos)

    def clicked_view(self, touch):
        if touch.button == "right":
            return
        if touch.button == "scrollup":
            self.world.camera.z -= 1
        elif touch.button == "scrolldown":
            self.world.camera.z += 1
        else:
            cx, cy = self.world.camera.x, self.world.camera.y
            tx, ty = touch.pos
            sx, sy = tx - cx, ty - cy
            x, y = config.transform_to_grid(sx, sy)
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

    def moved_view(self, touch):
        if touch.button == "right":
            self.world.camera.x += touch.dx
            self.world.camera.y += touch.dy

    def on_touch_down(self, touch):
        menu = self.ids["menu"]
        if menu.collide_point(*touch.pos):
            menu.on_touch_down(touch)
        else:
            self.clicked_view(touch)

    def on_touch_move(self, touch):
        menu = self.ids["menu"]
        if menu.collide_point(*touch.pos):
            menu.on_touch_move(touch)
        else:
            self.moved_view(touch)


