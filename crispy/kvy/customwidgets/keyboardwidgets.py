from kivy.uix.widget import Widget
from kivy.core.window import Window


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

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 261:
            print("center")
        if keycode[0] == 264:
            # North
            print("north")
        if keycode[0] == 258:
            # South
            print("south")

        if keycode[0] == 262:
            # East
            print("east")

        if keycode[0] == 260:
            # West
            print("west")

        if keycode[0] == 263:
            # North West
            print("northwest")

        if keycode[0] == 265:
            # North East
            print("northeast")

        if keycode[0] == 257:
            # South West
            print("southwest")

        if keycode[0] == 259:
            # South East
            print('southeast')

        return True


