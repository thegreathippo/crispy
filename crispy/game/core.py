from imbroglio import System
from customdicts import InvertibleDict, ReversibleDict, CustomDict
from .utils import Point3
from .utils import Sprite3
from .consoles import Console
import constants


class Cell3Dict(InvertibleDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Point3(*value))


class Pos3Dict(ReversibleDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Point3(*value))


class Sprite3Dict(CustomDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Sprite3(*value))


class World(System):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console("Initializing...")
        self._camera = None
        self._player = None
        self.focus = None
        self.setup()

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, entity):
        self._player = entity
        self.focus = entity

    @property
    def camera(self):
        return self._camera

    def spin(self, *args):
        if hasattr(self.focus, "energy"):
            while self.focus.energy < 0:
                self.processes()
                if not hasattr(self.focus, "energy"):
                    break

    def setup(self):
        kwargs = dict()
        kwargs["name"] = "Camera"
        kwargs["pos"] = 0, 0, 0
        camera = self.new_entity(**kwargs)
        self._camera = camera

    def clear(self):
        super().clear()
        self.setup()


world = World("name", "energy", "melee", "armor_class", "melee_bonus", "melee_damage", "max_hp", "damage",
              cell=Cell3Dict, pos=Pos3Dict, sprite=Sprite3Dict)

