import pickle
from .ecs import System
from utils import ObservedPoint
from utils import CellDict
from utils import PosDict
from utils import SpriteDict
import config
import constants


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
        self["sprite"] = SpriteDict()
        self["material"] = dict()
        self.camera = ObservedPoint(0, 0, 0)
        self.player = self.get_entity()
        self._focus = self.player.eid

    @property
    def focus(self):
        return self.get_entity(self._focus)

    @focus.setter
    def focus(self, entity_or_eid):
        if hasattr(entity_or_eid, "eid"):
            eid = entity_or_eid.eid
        else:
            eid = entity_or_eid
        self._focus = eid

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
            x, y, z = block.cell.x + vx, block.cell.y + vy, block.cell.z + vz
            block.cell = x, y, z
            block.sprite = x, y, z, constants.IMG_GRANITE
        except ValueError:
            return False
        return True

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
        eid_count = 1
        eid_translation = {0: 0} # 0 is always player
        with open(path, "rb") as f:
            data = pickle.load(f)
            for component in self:
                for eid in data[component]:
                    if eid not in eid_translation:
                        eid_translation[eid] = eid_count
                        eid_count += 1
                    translated_eid = eid_translation[eid]
                    self[component][translated_eid] = data[component][eid]
        self.eid_count = eid_count

    def clear(self):
        for component in self:
            self[component].clear()
        self.eid_count = 0
        self.player = self.get_entity()
        self.focus = self.player


def get_coor(x, y=None, z=None):
    if y is not None:
        return x, y, z
    else:
        return x


world = World()
