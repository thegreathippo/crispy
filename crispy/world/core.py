from .compdicts import InverseDict, ReverseDict, CallbackDict
from .ecs import System


class Game(System):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cell"] = InverseDict()
        self["pos"] = ReverseDict()
        self["tile_pos"] = CallbackDict()
        self["tile_sprite"] = CallbackDict()
        self.camera = self.get_entity(pos=(0, 0, 0))
        self.player = None

    def fill(self, x, y=None, z=None, material=None):
        pos = get_coor(x, y, z)
        self.get_entity(cell=pos, material=material, tile_pos=pos)

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
    if y:
        return x, y, z
    else:
        return x


game = Game()

