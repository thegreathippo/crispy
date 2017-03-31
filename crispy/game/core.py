from .ecs import ProcessManager
from .objects import GameObject
from utils import InvertibleDict
from utils import ReversibleDict
from utils import TupleDict
from utils import Point3
from utils import Sprite3
import constants


class CellDict(TupleDict, InvertibleDict):
    cls = Point3


class PosDict(TupleDict, ReversibleDict):
    cls = Point3


class SpriteDict(TupleDict):
    cls = Sprite3


class World(ProcessManager):

    def __init__(self):
        super().__init__()
        self._focus = constants.EID_PLAYER

        class Entity(self.entity_cls, GameObject):
            pass

        self.entity_cls = Entity
        self["cell"] = CellDict()
        self["pos"] = PosDict()
        self["sprite"] = SpriteDict()
        self["energy"] = dict()
        self.clear()


    @property
    def player(self):
        return self.get_entity(constants.EID_PLAYER)

    @property
    def camera(self):
        return self.get_entity(constants.EID_CAMERA)

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
                self()

    def set_cell(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        cell = self.get_cell(x, y, z)
        if cell:
            return
        e = self.get_entity(cell=pos, **kwargs)
        return e

    def get_cell(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.get_entity(eid)

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
