from .utils import NULL


class CustomDict(dict):
    def __repr__(self):
        return type(self).__name__ + super().__repr__()

    def copy(self):
        return type(self)(*self.items())


class CollisionError(ValueError):
    def __init__(self, key1, val1, key2, val2):
        txt = "{0} cannot be mapped to {1}; {2} is mapped to it".format(
            key1, val2, key2)
        super().__init__(txt)
        self.blocked_key = key1
        self.blocking_key = key2
        self.blocking_value = val2
        if val1 is not NULL:
            self.blocked_value = val1


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
        if value in self.inverse and self.inverse[value] != item:
            item_val = self.get(item, NULL)
            raise CollisionError(item, item_val, self.inverse[value], value)
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
