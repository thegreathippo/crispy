class ComponentDict(dict):
    def __getitem__(self, key):
        if hasattr(key, "get_eid"):
            key = key.get_eid()
        return super().__getitem__(key)


class BaseEntity:
    root = None

    def __init__(self, _eid=None, **kwargs):
        if _eid is None:
            eid = self.root.eid
            self.root.eid += 1
        else:
            if hasattr(_eid, "get_eid"):
                _eid = _eid.get_eid()
            eid = _eid
        super().__setattr__("_eid", eid)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_eid(self):
        return self._eid

    def __getattr__(self, attr):
        value = None
        try:
            value = self.root[attr][self._eid]
        except KeyError:
            super().__getattribute__(attr)
        return value

    def __setattr__(self, attr, value):
        if attr not in self.root:
            self.root[attr] = ComponentDict()
        self.root[attr][self._eid] = value

    def __delattr__(self, attr):
        del self.root[attr][self._eid]
