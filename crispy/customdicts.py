from imbroglio import InnerDict

NULL = object()


class CustomDict(InnerDict):
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
    CollisionError = CollisionError

    def __init__(self):
        self.inverse = dict()
        super().__init__()

    def clear(self):
        super().clear()
        self.inverse.clear()

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
    def __init__(self):
        self.inverse = dict()
        super().__init__()

    def clear(self):
        super().clear()
        self.inverse.clear()

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

