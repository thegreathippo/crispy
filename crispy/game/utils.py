import collections

__all__ = ["Point3", "Sprite3"]

Point3 = collections.namedtuple("Point3", ["x", "y", "z"])
Sprite3 = collections.namedtuple("Sprite3", ["x", "y", "z", "image"])
