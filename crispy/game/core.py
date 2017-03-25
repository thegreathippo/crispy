import pickle
from .ecs import System
from utils import ObservedPoint
from utils import CellDict
from utils import PosDict
from utils import CallbackCellDict
import config


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
        self["image"] = dict()
        self["sprite"] = CallbackCellDict()
        self["material"] = dict()
        self.camera = ObservedPoint(0, 0, 0)
        self.player = None

    def set_block(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        block = self.get_block(x, y, z)
        if block:
            return
        e = self.get_entity(cell=pos, **kwargs)
        e.sprite = pos
        return e

    def get_block(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eid = self["cell"].inverse.get(pos, None)
        if eid is not None:
            return self.get_entity(eid)

    def del_block(self, block):
        del block.cell
        del block.sprite

    def move_block(self, block, vx, vy=None, vz=None):
        vx, vy, vz = get_coor(vx, vy, vz)
        try:
            x, y, z = block.cell.x + vx, block.cell.y + vy, block.cell.z + vz
            block.cell = x, y, z
            block.sprite = x, y, z
        except ValueError:
            return False
        return True

    def set_thing(self, x, y=None, z=None, **kwargs):
        pos = get_coor(x, y, z)
        thing = self.get_entity(pos=pos, sprite=pos, **kwargs)
        return thing

    def get_things(self, x, y=None, z=None):
        pos = get_coor(x, y, z)
        eids = self["pos"].reverse.get(pos, set())
        return {self.get_entity(eid) for eid in eids}

    def save(self, path=None):
        if not path:
            path = config.DEFAULT_SAVE_PATH
        save_dict = dict()
        for c in self:
            save_dict[c] = dict(self[c])
        with open(path, "wb") as f:
            pickle.dump(save_dict, f, pickle.HIGHEST_PROTOCOL)

    def load(self, path=None):
        if not path:
            path = config.DEFAULT_SAVE_PATH
        self.clear()
        eid_count = 0
        with open(path, "rb") as f:
            data = pickle.load(f)
            for component in self:
                for eid in data[component]:
                    if eid > eid_count:
                        eid_count = eid
                    self[component][eid] = data[component][eid]
        self.eid_count = eid_count + 1

    def clear(self):
        for component in self:
            self[component].clear()
        self.eid_count = 0


def get_coor(x, y=None, z=None):
    if y is not None:
        return x, y, z
    else:
        return x


world = World()
