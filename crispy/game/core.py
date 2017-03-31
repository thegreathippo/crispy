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
        self()

    def set_block(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        block = self.get_block(x, y, z)
        if block:
            return
        e = self.get_entity(cell=pos, **kwargs)
        return e

    def get_block(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.get_entity(eid)

    def move_block(self, block, vx, vy=None, vz=None):
        # this method is actually static; we can eventually move it
        # elsewhere
        vx, vy, vz = get_coor(vx, vy, vz)
        try:
            x, y, z = block.cell[0] + vx, block.cell[1] + vy, block.cell[2] + vz
            block.cell = x, y, z
            try:
                block.sprite = x, y, z, block.sprite[3]
            except AttributeError:
                pass
        except ValueError:
            return False
        return True

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
