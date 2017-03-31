from kivy.uix.widget import Widget
from kivy.core.window import Window
import constants


class KeyboardWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_input(self, user_input):
        pass

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 261:
            self.on_input(constants.INPUT_NONE)
        if keycode[0] == 264:
            # North
            self.on_input(constants.INPUT_NORTH)
        if keycode[0] == 258:
            # South
            self.on_input(constants.INPUT_SOUTH)

        if keycode[0] == 262:
            # East
            self.on_input(constants.INPUT_EAST)

        if keycode[0] == 260:
            # West
            self.on_input(constants.INPUT_WEST)

        if keycode[0] == 263:
            # North West
            self.on_input(constants.INPUT_NORTH_WEST)

        if keycode[0] == 265:
            # North East
            self.on_input(constants.INPUT_NORTH_EAST)

        if keycode[0] == 257:
            # South West
            self.on_input(constants.INPUT_SOUTH_WEST)

        if keycode[0] == 259:
            # South East
            self.on_input(constants.INPUT_SOUTH_EAST)

        return True


