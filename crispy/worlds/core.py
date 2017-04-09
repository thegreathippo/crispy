from ecs import ProcessManager
from .objects import WorldObject
from ecs import InvertibleDict
from ecs import ReversibleDict
from ecs import CallbackDict
from .utils import Point3
from .utils import Sprite3
import constants


class Cell3Dict(InvertibleDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Point3(*value))


class Pos3Dict(ReversibleDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Point3(*value))


class Sprite3Dict(CallbackDict):
    def __setitem__(self, item, value):
        super().__setitem__(item, Sprite3(*value))


class World(ProcessManager):

    def __init__(self):
        super().__init__()

        class WorldEntity(self.Entity, WorldObject):
            pass

        self.Entity = WorldEntity
        self._focus = constants.EID_PLAYER
        self["name"] = dict()
        self["cell"] = Cell3Dict()
        self["pos"] = Pos3Dict()
        self["sprite"] = Sprite3Dict(self)
        self["energy"] = dict()
        self["melee"] = dict()
        self["armor_class"] = dict()
        self["melee_bonus"] = dict()
        self["melee_damage"] = dict()
        self["max_hp"] = dict()
        self["damage"] = dict()
        self.clear()

    @property
    def player(self):
        return self.Entity(constants.EID_PLAYER)

    @property
    def camera(self):
        return self.Entity(constants.EID_CAMERA)

    @property
    def focus(self):
        return self.Entity(self._focus)

    @focus.setter
    def focus(self, entity_or_eid):
        eid = get_eid(entity_or_eid)
        self._focus = eid

    def spin(self, *args):
        if hasattr(self.focus, "energy"):
            while self.focus.energy < 0:
                self()

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
        e = self.Entity(**kwargs)
        return e

    def set_cell(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        cell = self.get_cell(x, y, z)
        if cell:
            return
        e = self.Entity(cell=pos, **kwargs)
        return e

    def get_cell(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.Entity(eid)

    def clear(self, entity=None):
        super().clear(entity)
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

world = World()
