import collections


def entity_cls(name, components):
    slots = list(components) + ["_eid"]
    return type(name, (EntityBase,), {"_root": components, "__slots__": slots})


class EntityBase:
    _root = dict()

    def __init__(self, eid, **kwargs):
        super().__setattr__("_eid", eid)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def root(self):
        return self._root

    @property
    def eid(self):
        return self._eid

    def __setattr__(self, attr, value):
        try:
            self.root[attr][self.eid] = value
        except KeyError:
            raise AttributeError("{0} has no attribute {1}".format(self, attr))

    def __getattr__(self, attr):
        try:
            return self.root[attr][self.eid]
        except KeyError:
            raise AttributeError("{0} has no attribute {1}".format(self, attr))

    def __delattr__(self, attr):
        try:
            del self.root[attr][self.eid]
        except KeyError:
            raise AttributeError("{0} has no attribute {1}".format(self, attr))

    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, self.eid)

    def __eq__(self, other):
        try:
            return (other.eid, other.root) == (self.eid, self.root)
        except AttributeError:
            return False


def _get_zero():
    return 0


class EidRef(collections.defaultdict):
    def __init__(self):
        super().__init__(_get_zero)
        self.free = set()

    def increment(self, eid):
        self[eid] += 1
        self.free.discard(eid)

    def decrement(self, eid):
        self[eid] -= 1
        if self[eid] <= 0:
            del self[eid]
            self.free.add(eid)

    def get_next(self):
        if self.free:
            return self.free.pop()
        return len(self)

    def clear(self):
        super().clear()
        self.free.clear()
