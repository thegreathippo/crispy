import collections

NULL = object()


class OuterDict(collections.UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        components = {k: InnerDict for k in args}
        components.update(kwargs)
        for k, v in components.items():
            self[k] = v()


class InnerDict(collections.UserDict):
    def __init__(self):
        super().__init__()
        self._on_new = list()
        self._on_change = list()
        self._on_del = list()

    def bind_new(self, func):
        self._on_new.append(func)

    def bind_change(self, func):
        self._on_change.append(func)

    def bind_del(self, func):
        self._on_del.append(func)

    def on_new(self, key, value):
        for func in self._on_new:
            func(key, value)

    def on_change(self, key, old_value, new_value):
        for func in self._on_change:
            func(key, old_value, new_value)

    def on_del(self, key):
        for func in self._on_del:
            func(key)

    def __setitem__(self, item, value):
        old_value = self.data.get(item, NULL)
        if old_value != value:
            self.data[item] = value
            if old_value is NULL:
                self.on_new(item, value)
            else:
                self.on_change(item, old_value, value)

    def __delitem__(self, item):
        del self.data[item]
        self.on_del(item)

    def __repr__(self):
        return type(self).__name__ + str(self.data)

