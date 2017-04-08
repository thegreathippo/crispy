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
        data += " # of Cell EIDs:   {}\n".format(len(self.world["cell"]))
        data += " # of Sprite EIDs: {}\n".format(len(self.world["sprite"]))
        data += " Player EID:       {}\n".format(self.world.player.eid)
        data += " Focus EID:        {}\n".format(self.world.focus.eid)
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

        world["sprite"].bind_new(view.load_sprite)
        world["sprite"].bind_del(view.unload_sprite)
        world["sprite"].bind_change(view.change_sprite)

        world.player.cell = 0, 0, 0
        world.player.sprite = 0, 0, 0, constants.IMG_PLAYER
        world.player.energy = 0
        world.player.melee = 5
        world.player.armor_class = 5
        world.player.melee_bonus = 1
        world.player.melee_damage = [1, 10]
        world.player.hp = 10
        world.player.max_hp = 10

        self.view = view
        self.menu = menu
        self.mode = None

    def on_input(self, user_input):
        vx, vy, vz = constants.DIRECTIONS[user_input]
        self.world.move_cell(self.world.focus, vx, vy, vz)

    def on_tap(self, x, y, z, block):
        if self.mode in constants.EDIT_DRAW_MODES:
            image = constants.IMG_GRANITE
            kwargs = dict()
            if self.mode == constants.EDIT_MODE_FLOOR:
                z -= 1
            elif self.mode == constants.EDIT_MODE_MONSTER:
                image = constants.IMG_MONSTER
                kwargs["energy"] = 0
                kwargs["melee"] = 0
                kwargs["armor_class"] = 0
                kwargs["melee_bonus"] = 0
                kwargs["melee_damage"] = [1, 6]
                kwargs["hp"] = 10
                kwargs["max_hp"] = 10
            sprite = x, y, z, image
            self.world.set_cell(x, y, z, sprite=sprite, **kwargs)
        elif self.mode == constants.EDIT_MODE_PLAYER:
            self.world.player.cell = x, y, z
            sprite = x, y, z, constants.IMG_PLAYER
            self.world.player.sprite = sprite
        elif block:
            if self.mode == constants.EDIT_MODE_ERASE:
                block.clear()
            elif self.mode == constants.EDIT_MODE_SELECT:
                self.world.focus = block

    def on_touch_down(self, touch):
        if self.menu.collide_point(*touch.pos):
            self.menu.on_touch_down(touch)
        else:
            x, y = kvy.get_touched_cell(touch.pos, self.world.camera.pos)
            z = self.world.camera.z
            cell = self.world.get_cell(x, y, z)
            if not cell:
                cell = self.world.get_cell(x, y, z - 1)
            self.on_tap(x, y, z, cell)
