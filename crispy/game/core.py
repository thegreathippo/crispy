from .ecs import System
from utils import CellDict
from utils import CallbackDict
from utils import PosDict


class World(System):
    def __init__(self):
        super().__init__()

        class Entity(self.entity_cls):
            @property
            def x(self):
                return self.pos[0]

            @property
            def y(self):
                return self.pos[1]

            @property
            def z(self):
                return self.pos[2]

        self.entity_cls = Entity
        self["cell"] = CellDict()
        self["pos"] = PosDict()
        self["tile"] = CallbackDict()
        self["sprite"] = CallbackDict()
        self.camera = 0, 0, 0
        self.player = None

    def fill(self, *args, material=None):
        for pos in args:
            self.set_block(pos, material)

    def set_block(self, x, y=None, z=None, material=None):
        pos = get_coor(x, y, z)
        return self.get_entity(cell=pos, material=material, tile=pos)

    def get_block(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.get_entity(eid)

    def get_things(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eids = self["pos"].reverse.get(pos, set())
        return {self.get_entity(eid) for eid in eids}


def get_coor(x, y=None, z=None):
    if y is not None:
        return x, y, z
    else:
        return x


world = World()
