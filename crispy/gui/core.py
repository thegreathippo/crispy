import constants
import kvy
import gamerules
import worlds
world = worlds.world
import gui.layers


class GameApp(kvy.App):
    world = world
    console_text = kvy.StringProperty(" \n Initializing...\n ")

    def build(self):
        window = GameWindow(world)
        kvy.schedule_interval(world.spin)
        return window

    def add_to_console(self, text):
        try:
            self.console_text += "\n" + text
        except TypeError:
            self.console_text += "\n" + str(text)


class GameWindow(kvy.KeyboardWidget, kvy.FloatLayout):

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        view = self.ids["view_screen"]
        menu = self.ids["menu"]

        world["sprite"].bind_new(view.load_sprite)
        world["sprite"].bind_del(view.unload_sprite)
        world["sprite"].bind_change(view.change_sprite)

        world.set_player(0, 0, 0)

        self.view = view
        self.menu = menu
        self.mode = None

    def on_input(self, user_input):
        direction = constants.DIRECTIONS[user_input]
        try:
            gamerules.movement.steps[direction](world.focus)
        except ValueError as e:
            entity = world.Entity(e.blocking_key)
            if hasattr(entity, "damage"):
                sword = world.Entity(melee_bonus=2, melee_damage=["slashing", 1, 6])
                melee = gamerules.attacks.Melee(world.focus, sword, entity)
                app.add_to_console(melee.check)

    def on_tap(self, x, y, z, block):
        if self.mode in constants.EDIT_DRAW_MODES:
            if self.mode == constants.EDIT_MODE_MONSTER:
                world.set_agent(x, y, z)
                return
            image = constants.IMG_GRANITE
            kwargs = dict()
            if self.mode == constants.EDIT_MODE_FLOOR:
                z -= 1
            sprite = x, y, z, image
            world.set_cell(x, y, z, sprite=sprite, **kwargs)
        elif self.mode == constants.EDIT_MODE_PLAYER:
            world.player.cell = x, y, z
            sprite = x, y, z, constants.IMG_PLAYER
            world.player.sprite = sprite
        elif block:
            if self.mode == constants.EDIT_MODE_ERASE:
                world.clear(block)
            elif self.mode == constants.EDIT_MODE_SELECT:
                world.focus = block

    def on_touch_down(self, touch):
        if self.menu.collide_point(*touch.pos):
            self.menu.on_touch_down(touch)
        else:
            x, y = kvy.get_touched_cell(touch.pos, world.camera.pos)
            z = world.camera.z
            cell = world.get_cell(x, y, z)
            if not cell:
                cell = world.get_cell(x, y, z - 1)
            self.on_tap(x, y, z, cell)


app = GameApp()
