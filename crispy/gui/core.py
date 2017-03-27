import utils
import constants
import gui.layers
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import StringProperty


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
        data += " Player EID:       {}\n".format(self.world.player.eid)
        data += " Focus EID:        {}\n".format(self.world.focus.eid)
        data += " Player In:        {}\n".format(self.world.player.initiative)
        if hasattr(self.world.player, "cell"):
            data += " Player Cell:   {}\n".format(self.world.player.cell)
        if hasattr(self.world.camera, "pos"):
            data += " Camera Position:  {}\n".format(self.world.camera.pos)
        return data

    def build(self):
        window = GameWindow(self.world)

        def get_debug_data(*args):
            window.debug_data = self.get_debug_data()

        utils.schedule_interval(get_debug_data, 0.1)
        utils.schedule_interval(self.world.spin, 0)
        return window


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
        self.mode = None

        def follow_camera(*args):
            if hasattr(world.camera, "pos"):
                self.view.follow_camera(world.camera)

        utils.schedule_interval(follow_camera, 0)

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def load_sprite(self, eid, pos):
        entity = self.world.get_entity(eid)
        self.view.load_sprite(entity)

    def clicked_view(self, touch):
        if touch.button == "right":
            x, y = utils.get_touched_cell(touch.pos, self.world.camera)
            self.world.camera.x = x
            self.world.camera.y = y
        elif touch.button == "scrollup":
            self.world.camera.z -= 1
        elif touch.button == "scrolldown":
            self.world.camera.z += 1
        else:
            x, y = utils.get_touched_cell(touch.pos, self.world.camera)
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
                block = self.world.get_block(x, y, 1)
                if not block:
                    self.world.player.cell = (x, y, 1)
                    self.world.player.sprite = x, y, 1, constants.IMG_PLAYER
                    self.world.player.initiative = 0
            elif self.mode is constants.MODE_DRAW_MONSTER:
                sprite = x, y, 1, constants.IMG_MONSTER
                self.world.set_block(x, y, 1, sprite=sprite, initiative=0)
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

    def on_touch_down(self, touch):
        menu = self.ids["menu"]
        if menu.collide_point(*touch.pos):
            menu.on_touch_down(touch)
        else:
            self.clicked_view(touch)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 261:
            self.world.focus.initiative -= 10
        if keycode[0] == 264:
            # North
            move = self.world.move_block(self.world.focus, 0, 1, 0)
        if keycode[0] == 258:
            # South
            move = self.world.move_block(self.world.focus, 0, -1, 0)

        if keycode[0] == 262:
            # East
            move = self.world.move_block(self.world.focus, 1, 0, 0)

        if keycode[0] == 260:
            # West
            move = self.world.move_block(self.world.focus, -1, 0, 0)

        if keycode[0] == 263:
            # North West
            move = self.world.move_block(self.world.focus, -1, 1, 0)

        if keycode[0] == 265:
            # North East
            move = self.world.move_block(self.world.focus, 1, 1, 0)

        if keycode[0] == 257:
            # South West
            move = self.world.move_block(self.world.focus, -1, -1, 0)

        if keycode[0] == 259:
            # South East
            move = self.world.move_block(self.world.focus, 1, -1, 0)

        self.world.camera.pos = self.world.focus.cell

        return True





