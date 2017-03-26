from .customdicts import *
import collections
import config


Point3 = collections.namedtuple("Point3", ["x", "y", "z"])


def transform_to_grid(x, y):
    ret_x = int(x // config.TILE_SIZE)
    ret_y = int(y // config.TILE_SIZE)
    return ret_x, ret_y


def transform_to_screen(x, y):
    ret_x = x * config.TILE_SIZE
    ret_y = y * config.TILE_SIZE
    return ret_x, ret_y


class ObservedPoint:

    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z
        self.observers = list()

    def register(self, func):
        self.observers.append(func)

    @property
    def pos(self):
        return Point3(self.x, self.y, self.z)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        old_pos = self.pos
        self._x = int(x)
        for observer in self.observers:
            observer(old_pos, self.pos)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        old_pos = self.pos
        self._y = int(y)
        for observer in self.observers:
            observer(old_pos, self.pos)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        old_pos = self.pos
        self._z = int(z)
        for observer in self.observers:
            observer(old_pos, self.pos)
