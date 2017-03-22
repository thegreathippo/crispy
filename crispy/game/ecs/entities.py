from utils import InternalDict


class BaseEntity:
    def __init__(self, *args, **kwargs):
        root = args[0]
        try:
            eid = args[1]
        except IndexError:
            eid = root.eid_count
            root.eid_count += 1
        self.__dict__["root"] = root
        self.eid = eid
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __getattr__(self, attr):
        try:
            value = self.root[attr][self.eid]
        except KeyError:
            return super().__getattribute__(attr)
        return value

    def __setattr__(self, attr, value):
        if attr not in self.root:
            super().__setattr__(attr, value)
        else:
            self.root[attr][self.eid] = value

    def __delattr__(self, attr):
        try:
            super().__delattr__(attr)
        except AttributeError:
            del self.root[attr][self.eid]

    def __eq__(self, other):
        try:
            return (other.eid, other.root.rid) == (self.eid, self.root.rid)
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.eid, self.root.rid))


class Root(InternalDict):
    rid = 0
    entity_cls = BaseEntity

    def __init__(self):
        super().__init__()
        self.rid = self.rid
        type(self).rid += 1
        self.eid_count = 0

    def get_entity(self, eid=None, **kwargs):
        if eid is None:
            return self.entity_cls(self, **kwargs)
        else:
            return self.entity_cls(self, eid, **kwargs)
