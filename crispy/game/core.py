from imbroglio import System
from customdicts import InvertibleDict, ReversibleDict, CustomDict
from .utils import Point3
from .utils import Sprite3
from .consoles import Console
import constants


PLAYER_EID = 1
CAMERA_EID = 0


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
        self._focus = PLAYER_EID
        self.clear()


    @property
    def player(self):
        return self.get_entity(PLAYER_EID)

    @property
    def camera(self):
        return self.get_entity(CAMERA_EID)

    @property
    def focus(self):
        return self.get_entity(self._focus)

    @focus.setter
    def focus(self, entity_or_eid):
        eid = get_eid(entity_or_eid)
        self._focus = eid

    def spin(self, *args):
        if hasattr(self.focus, "energy"):
            while self.focus.energy < 0:
                self.processes()
                if not hasattr(self.focus, "energy"):
                    break

    def set_player(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        cell = self.get_cell(x, y, z)
        if cell:
            return
        kwargs["name"] = "Player"
        kwargs["cell"] = pos
        kwargs["sprite"] = x, y, z, constants.IMG_PLAYER
        kwargs["energy"] = 0
        kwargs["melee"] = 5
        kwargs["armor_class"] = 0
        kwargs["damage"] = 0
        kwargs["max_hp"] = 10
        for k in kwargs:
            setattr(self.player, k, kwargs[k])

    def set_agent(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        cell = self.get_cell(x, y, z)
        if cell:
            return
        kwargs["name"] = "Monster"
        kwargs["sprite"] = x, y, z, constants.IMG_MONSTER
        kwargs["energy"] = 0
        kwargs["melee"] = 5
        kwargs["armor_class"] = 0
        kwargs["damage"] = 0
        kwargs["max_hp"] = 10
        kwargs["cell"] = pos
        e = self.new_entity(**kwargs)
        return e

    def set_cell(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        cell = self.get_cell(x, y, z)
        if cell:
            return
        e = self.new_entity(cell=pos, **kwargs)
        return e

    def get_cell(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.get_entity(eid)

    def clear(self):
        super().clear()
        camera = self.new_entity()
        self.eids.increment(camera.eid)
        player = self.new_entity()
        self.eids.increment(player.eid)
        self.set_player(0, 0, 0)
        self.camera.pos = 0, 0, 0
        self.focus = self.player


def get_coor(x, y=None, z=None):
    if y is not None:
        return x, y, z
    else:
        return x


def get_eid(entity_or_eid):
    if hasattr(entity_or_eid, "eid"):
        eid = entity_or_eid.eid
    else:
        eid = entity_or_eid
    return eid

world = World("name", "energy", "melee", "armor_class", "melee_bonus", "melee_damage", "max_hp", "damage", "dead",
              cell=Cell3Dict, pos=Pos3Dict, sprite=Sprite3Dict)

