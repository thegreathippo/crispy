
__all__ = ["TupleDict", "InvertibleDict", "ReversibleDict"]
NULL = object()


class CustomDict(dict):
    def __repr__(self):
        return type(self).__name__ + super().__repr__()

    def copy(self):
        return type(self)(*self.items())


class TupleDict(CustomDict):
    cls = tuple

    def copy(self):
        instance = type(self)()
        for k, v in self.items():
            instance[k] = self.cls(*v)
        return instance

    def __setitem__(self, item, value):
        super().__setitem__(item, self.cls(*value))


class InvertibleDict(CustomDict):
    def __init__(self, other=None, *args):
        super().__init__()
        self.inverse = dict()
        if other:
            try:
                k, v = other
                self[k] = v
            except TypeError:
                k, v = other.items()
                self[k] = v
        for arg in args:
            k, v = arg
            self[k] = v

    def clear(self):
        super().clear()
        self.inverse.clear()

    def pop(self, key, default=NULL):
        if default is not NULL:
            value = super().pop(key, default)
        else:
            value = super().pop(key)
        if value != default:
            del self.inverse[value]
        return value

    def popitem(self):
        key, value = super().popitem()
        del self.inverse[value]
        return key, value

    def update(self, other=None, **kwargs):
        if other:
            try:
                for k, v in other:
                    self[k] = v
            except TypeError:
                for k, v in other.items():
                    self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def __setitem__(self, item, value):
        if value in self.inverse:
            raise ValueError("{0} cannot be mapped to {1}; is already "
                             "mapped to {2}".format(value, item,
                                                    self.inverse[value]))
        if item in self:
            del self.inverse[self[item]]
        super().__setitem__(item, value)
        self.inverse[self[item]] = item

    def __delitem__(self, item):
        value = self[item]
        del self.inverse[value]
        super().__delitem__(item)


class ReversibleDict(CustomDict):
    def __init__(self, other=None, *args):
        super().__init__()
        self.inverse = dict()
        if other:
            try:
                k, v = other
                self[k] = v
            except TypeError:
                k, v = other.items()
                self[k] = v
        for arg in args:
            k, v = arg
            self[k] = v

    def clear(self):
        super().clear()
        self.inverse.clear()

    def pop(self, key, default=NULL):
        if default is not NULL:
            value = super().pop(key, default)
        else:
            value = super().pop(key)
        if value != default:
            del self.inverse[value]
        return value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def update(self, other=None, **kwargs):
        if other:
            try:
                for k, v in other:
                    self[k] = v
            except TypeError:
                for k, v in other.items():
                    self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, item, value):
        if item in self:
            old_value = self[item]
            self.inverse[old_value].remove(item)
            if not self.inverse[old_value]:
                del self.inverse[old_value]
        if value not in self.inverse:
            self.inverse[value] = set()
        super().__setitem__(item, value)
        self.inverse[value].add(item)

    def __delitem__(self, item):
        value = self[item]
        self.inverse[value].remove(item)
        if not self.inverse[value]:
            del self.inverse[value]
        super().__delitem__(item)

    def popitem(self):
        key, value = super().popitem()
        self.inverse[value].remove(key)
        if not self.inverse[value]:
            del self.inverse[value]
        return key, value





