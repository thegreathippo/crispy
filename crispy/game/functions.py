from .core import world
import constants


CREATURE_DEFAULTS = {
    "name": "Creature",
    "energy": 0,
    "melee": 1,
    "armor_class": 0,
    "damage": 0,
    "max_hp": 10
}


def set_player(entity):
    world.player = entity


def add_creature(x, y=None, z=None, **attributes):
    pos = get_coor(x, y, z)
    cell = get_cell(x, y, z)
    if cell:
        return
    kwargs = dict()
    kwargs.update(CREATURE_DEFAULTS)
    kwargs["sprite"] = x, y, z, constants.IMG_MONSTER
    kwargs["cell"] = pos
    kwargs.update(attributes)
    creature = world.new_entity(**kwargs)
    return creature


def add_block(x, y=None, z=None, **attributes):
    pos = get_coor(x, y, z)
    cell = get_cell(x, y, z)
    if cell:
        return
    kwargs = dict()
    kwargs["sprite"] = x, y, z, constants.IMG_GRANITE
    kwargs["cell"] = pos
    kwargs.update(attributes)
    block = world.new_entity(**kwargs)
    return block


def get_cell(x, y=None, z=None):
    pos = get_coor(x, y, z)
    eid = world["cell"].inverse.get(pos, None)
    if eid is not None:
        return world.get_entity(eid)


def get_coor(x, y=None, z=None):
    if y is not None:
        return x, y, z
    else:
        return x


