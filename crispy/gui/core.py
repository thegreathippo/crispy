import gui.layers
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
import utils
import constants
import config


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

kivy.require("1.9.0")


class GameApp(App):

    def __init__(self, world):
        super().__init__()
        self.world = world

    def get_debug_data(self):
        data = ""
        data += " # of Components:  {}\n".format(len(self.world))
        data += " EID Counter:      {}\n".format(self.world.eid_count)
        data += " # of Cell EIDs:   {}\n".format(len(self.world["cell"]))
        data += " # of Sprite EIDs: {}\n".format(len(self.world["sprite"]))
        data += " Camera Position:  {}\n".format(self.world.camera.pos)
        if hasattr(self.world.player, "cell"):
            data += "Player Position:   {}\n".format(self.world.player.cell)
        return data

    def build(self):
        window = GameWindow(self.world)

        def get_debug_data(dt):
            window.debug_data = self.get_debug_data()

        Clock.schedule_interval(get_debug_data, 0.1)
        return window

    def clicked_view(self, touch):
        pass


class GameWindow(FloatLayout):
    debug_data = StringProperty()

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.view = self.ids["view_screen"]
        self.menu = self.ids["menu"]
        world["sprite"].on_new = self.load_sprite
        world["sprite"].on_del = self.view.remove_sprite
        world["sprite"].on_change = self.view.move_sprite
        world.camera.register(self.move_camera)
        self.mode = None
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def load_sprite(self, eid, pos):
        entity = self.world.get_entity(eid)
        self.ids["view_screen"].load_sprite(entity)

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
            x, y = utils.transform_to_grid(sx, sy)

            if self.mode is constants.MODE_DRAW_ROOF:
                sprite = x, y, 2, constants.IMG_GRANITE
                self.world.set_block(x, y, 2, sprite=sprite)
            elif self.mode is constants.MODE_DRAW_WALL:
                sprite = x, y, 1, constants.IMG_GRANITE
                self.world.set_block(x, y, 1, sprite=sprite)
            elif self.mode is constants.MODE_DRAW_FLOOR:
                sprite = x, y, 0, constants.IMG_GRANITE
                self.world.set_block(x, y, 0, sprite=sprite)
            elif self.mode is constants.MODE_DRAW_PLAYER:
                self.world.player.cell = (x, y, 1)
                self.world.player.sprite = x, y, 1, constants.IMG_PLAYER
            elif self.mode is constants.MODE_DRAW_MONSTER:
                sprite = x, y, 1, constants.IMG_MONSTER
                self.world.set_block(x, y, 1, sprite=sprite)
            else:
                block = self.world.get_block(x, y, 2)
                if block is None:
                    block = self.world.get_block(x, y, 1)
                if block is None:
                    block = self.world.get_block(x, y, 0)
                if block:
                    if self.mode is constants.MODE_ERASE:
                        block.clear()
                    elif self.mode is constants.MODE_CHANGE_FOCUS:
                        self.world.focus = block

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

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 264:
            # North
            move = self.world.move_block(self.world.focus, 0, 1, 0)
            if move:
                self.world.camera.y -= config.TILE_SIZE
        if keycode[0] == 258:
            # South
            move = self.world.move_block(self.world.focus, 0, -1, 0)
            if move:
                self.world.camera.y += config.TILE_SIZE

        if keycode[0] == 262:
            # East
            move = self.world.move_block(self.world.focus, 1, 0, 0)
            if move:
                self.world.camera.x -= config.TILE_SIZE

        if keycode[0] == 260:
            # West
            move = self.world.move_block(self.world.focus, -1, 0, 0)
            if move:
                self.world.camera.x += config.TILE_SIZE

        if keycode[0] == 263:
            # North West
            move = self.world.move_block(self.world.focus, -1, 1, 0)
            if move:
                self.world.camera.x += config.TILE_SIZE
                self.world.camera.y -= config.TILE_SIZE

        if keycode[0] == 265:
            # North East
            move = self.world.move_block(self.world.focus, 1, 1, 0)
            if move:
                self.world.camera.x -= config.TILE_SIZE
                self.world.camera.y -= config.TILE_SIZE

        if keycode[0] == 257:
            # South West
            move = self.world.move_block(self.world.focus, -1, -1, 0)
            if move:
                self.world.camera.x += config.TILE_SIZE
                self.world.camera.y += config.TILE_SIZE

        if keycode[0] == 259:
            # South East
            move = self.world.move_block(self.world.focus, 1, -1, 0)
            if move:
                self.world.camera.x -= config.TILE_SIZE
                self.world.camera.y += config.TILE_SIZE




#        print('The key', keycode, 'have been pressed')
#        print(' - text is %r' % text)
#        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
#        if keycode[1] == 'escape':
#            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True





