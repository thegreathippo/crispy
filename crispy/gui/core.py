import utils
import constants
import kvy
import gui.layers


class GameApp(kvy.App):

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
        if hasattr(self.world.player, "cell"):
            data += " Player Cell:   {}\n".format(self.world.player.cell)
        if hasattr(self.world.camera, "pos"):
            data += " Camera Position:  {}\n".format(self.world.camera.pos)
        return data

    def build(self):
        window = GameWindow(self.world)

        def get_debug_data(*args):
            window.debug_data = self.get_debug_data()

        kvy.schedule_interval(get_debug_data)
        kvy.schedule_interval(self.world.spin)
        return window


class GameWindow(kvy.KeyboardWidget, kvy.FloatLayout):
    debug_data = kvy.StringProperty()

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        view = self.ids["view_screen"]
        menu = self.ids["menu"]

        world.bind_new("sprite", view.load_sprite, send_eid=False)
        world.bind_del("sprite", view.unload_sprite, send_eid=False)
        world.bind_change("sprite", view.change_sprite, send_eid=False)

        world.player.cell = 0, 0, 0
        world.player.sprite = 0, 0, 0, constants.IMG_PLAYER

        self.view = view
        self.menu = menu
        self.mode = None

    def on_input(self, user_input):
        vx, vy, vz = constants.DIRECTIONS[user_input]
        player = self.world.player
        x, y, z = player.x + vx, player.y + vy, player.z + vz
        try:
            player.cell = x, y, z
            player.sprite = x, y, z, player.sprite.image
        except ValueError:
            pass

    def on_tap(self, x, y, z, block):
        if self.mode in constants.EDIT_DRAW_MODES:
            image = constants.IMG_GRANITE
            if self.mode == constants.EDIT_MODE_FLOOR:
                z -= 1
            elif self.mode == constants.EDIT_MODE_MONSTER:
                image = constants.IMG_MONSTER
            sprite = x, y, z, image
            self.world.set_block(x, y, z, sprite=sprite)
        elif self.mode == constants.EDIT_MODE_PLAYER:
            self.world.player.cell = x, y, z
            sprite = x, y, z, constants.IMG_PLAYER
            self.world.player.sprite = sprite
        elif self.mode == constants.EDIT_MODE_ERASE and block:
            block.clear()

    def on_touch_down(self, touch):
        if self.menu.collide_point(*touch.pos):
            self.menu.on_touch_down(touch)
        else:
            x, y = kvy.get_touched_cell(touch.pos, self.world.camera.pos)
            z = self.world.camera.z
            block = self.world.get_block(x, y, z)
            if not block:
                block = self.world.get_block(x, y, z - 1)
            self.on_tap(x, y, z, block)
