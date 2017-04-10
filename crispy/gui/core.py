import constants
import kvy
import actions
import game
import gui.layers


class GameApp(kvy.App):
    world = game.world

    def build(self):
        window = GameWindow()
        kvy.schedule_interval(self.world.spin)
        return window


class GameWindow(kvy.KeyboardWidget, kvy.FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        view = self.ids["view_screen"]
        menu = self.ids["menu"]
        console = self.ids["console"]

        app.world["sprite"].bind_new(view.load_sprite)
        app.world["sprite"].bind_del(view.unload_sprite)
        app.world["sprite"].bind_change(view.change_sprite)

        app.world.set_player(0, 0, 0)

        self.view = view
        self.menu = menu
        self.console = console
        self.mode = None

        kvy.schedule_interval(self.update_console)

    def update_console(self, *args):
        self.console.text = app.world.console.get()

    def on_input(self, user_input):
        direction = constants.DIRECTIONS[user_input]
        actions.movement.steps[direction](app.world.focus)

    def on_tap(self, x, y, z, block):
        if self.mode in constants.EDIT_DRAW_MODES:
            if self.mode == constants.EDIT_MODE_MONSTER:
                app.world.set_agent(x, y, z)
                return
            image = constants.IMG_GRANITE
            kwargs = dict()
            if self.mode == constants.EDIT_MODE_FLOOR:
                z -= 1
            sprite = x, y, z, image
            app.world.set_cell(x, y, z, sprite=sprite, **kwargs)
        elif self.mode == constants.EDIT_MODE_PLAYER:
            app.world.player.cell = x, y, z
            sprite = x, y, z, constants.IMG_PLAYER
            app.world.player.sprite = sprite
        elif block:
            if self.mode == constants.EDIT_MODE_ERASE:
                app.world.clear(block)
            elif self.mode == constants.EDIT_MODE_SELECT:
                app.world.focus = block

    def on_touch_down(self, touch):
        if self.menu.collide_point(*touch.pos):
            self.menu.on_touch_down(touch)
        else:
            x, y = kvy.get_touched_cell(touch.pos, app.world.camera.pos)
            z = app.world.camera.z
            cell = app.world.get_cell(x, y, z)
            if not cell:
                cell = app.world.get_cell(x, y, z - 1)
            self.on_tap(x, y, z, cell)


app = GameApp()
