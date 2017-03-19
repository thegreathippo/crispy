"""TODO:
  * Should 'eid' be semi-private (IE, '_eid')? If so, 'root' too?
  * Need extensive testing for this module!
  * Need to have property setters override the __setattr__ for entities.

"""


class InternalDict:
    def __init__(self):
        self.data = dict()

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data

    def __setitem__(self, item, value):
        self.data[item] = value

    def __repr__(self):
        return str(self.data)


class BaseEntity:
    def __init__(self, *args, **kwargs):
        i = len(args)
        if i == 0:
            raise TypeError("__init__() takes 1 to 2 positional arguments but "
                            "0 were given")
        elif i == 1:
            root = args[0]
            eid = root.eid_count
            root.eid_count += 1
        elif i == 2:
            root = args[0]
            eid = args[1]
        else:
            raise TypeError("__init__() takes 1 to 2 positional arguments but "
                            "{} were given".format(i))
        super().__setattr__("_root", root)
        super().__setattr__("_eid", eid)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def eid(self):
        return self._eid

    @property
    def root(self):
        return self._root

    def __getattr__(self, attr):
        try:
            value = self.root[attr][self.eid]
        except KeyError:
            return super().__getattribute__(attr)
        return value

    def __setattr__(self, attr, value):
        if attr not in self.root:
            self.root[attr] = dict()
        component = self.root[attr]
        component[self.eid] = value

    def __delattr__(self, attr):
        component = self.root[attr]
        del component[self.eid]

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

    def __init__(self, **kwargs):
        super().__init__()
        self.rid = self.rid
        type(self).rid += 1
        self.eid_count = 0
        for component in kwargs:
            self[component] = kwargs[component]()

    def get_entity(self, eid=None, **kwargs):
        if eid is None:
            return self.entity_cls(self, **kwargs)
        else:
            return self.entity_cls(self, eid, **kwargs)
