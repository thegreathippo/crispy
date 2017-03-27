import pickle
from .ecs import System
from .objects import GameObject
from utils import CellDict
from utils import PosDict
from utils import SpriteDict
import config
import constants


class World(System):

    def __init__(self):
        super().__init__()
        self.eid_count = constants.EID_START_COUNT
        self._focus = constants.EID_PLAYER

        class Entity(self.entity_cls, GameObject):
            pass

        self.entity_cls = Entity
        self["cell"] = CellDict()
        self["pos"] = PosDict()
        self["sprite"] = SpriteDict()
        self["material"] = dict()
        self["initiative"] = dict()
        self.player.cell = 0, 0, 0
        self.setup()

    def setup(self):
        self.focus = self.player
        self.camera.pos = self.focus.cell

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
            block.sprite = x, y, z, block.sprite.image
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
        # note: The purpose of eid_translation is to 'clear out' unused eids (which occur when we clear eids).
        # however, the first few EIDs are reserved for special objects, hence why the translator starts with
        # a special dictionary (EID_TRANSLATION)
        if not path:
            path = config.DEFAULT_SAVE_PATH
        self.clear()
        eid_translation = dict(constants.EID_TRANSLATION)
        eid_count = constants.EID_START_COUNT
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
        self.setup()

    def clear(self, entity=None):
        if entity is not None:
            for component in self:
                try:
                    del self[component][entity.eid]
                except KeyError:
                    continue
        else:
            for component in self:
                self[component].clear()
            self.eid_count = constants.EID_START_COUNT


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
