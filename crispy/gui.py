import kivy
from kivy.app import App
from kivy.uix.widget import Widget

kivy.require("1.9.0")


class Game(App):

    def build(self):
        return CustomWidget()


class CustomWidget(Widget):
    pass


game = Game()

