import collections

Point3 = collections.namedtuple("Point3", ["x", "y", "z"])


class ZSorter:
    def __init__(self):
        self.obj_pos = dict()
        self.depth_map = dict()

    def add(self, obj, x, y=None, z=None):
        if y is None:
            x, y, z = x[0], x[1], x[2]
        self.obj_pos[obj] = Point3(x, y, z)
        if (x, y) not in self.depth_map:
            self.depth_map[(x, y)] = list()
        depth_map = self.depth_map[(x, y)]
        depth_map.append(obj)
        sorted(depth_map, key=lambda o: self.obj_pos[o].z)

    def remove(self, obj):
        x, y, z = self.obj_pos[obj]
        self.depth_map[(x, y)].remove(obj)

    def depth_of_field(self, x, y=None, z=None):
        if y is None:
            x, y, z = x[0], x[1], x[2]
        if (x, y) not in self.depth_map:
            return None
        for obj in self.depth_map[(x, y)]:
            if self.obj_pos[obj].z >= z:
                return obj

