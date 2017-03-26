import collections
import inspect

NULL = object()
Point3 = collections.namedtuple("Point3", ["x", "y", "z"])

__all__ = ["InternalDict", "CellDict", "PosDict", "CallbackDict", "CallbackPosDict",
           "CallbackCellDict"]


class InternalDict:
    def __init__(self):
        self.data = collections.OrderedDict()

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data

    def __setitem__(self, item, value):
        self.data[item] = value

    def __delitem__(self, item):
        del self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return str(self.data)


class CellDict(dict):
    value_cls = Point3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = dict()

    def __setitem__(self, item, value):
        value = self.value_cls(*value)
        if value in self.inverse:
            raise ValueError("{0} cannot be mapped to {1}; is already "
                             "mapped to {2}".format(value, item,
                                                    self.inverse[value]))
        if item in self:
            del self.inverse[self[item]]
        self.inverse[value] = item
        super().__setitem__(item, value)

    def __delitem__(self, item):
        value = self[item]
        del self.inverse[value]
        super().__delitem__(item)

    def clear(self):
        super().clear()
        self.inverse.clear()


class PosDict(dict):
    value_cls = Point3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = dict()

    def __setitem__(self, item, value):
        value = self.value_cls(*value)
        if item in self:
            old_value = self[item]
            self.inverse[old_value].remove(item)
            if not self.inverse[old_value]:
                del self.inverse[old_value]
        if value not in self.inverse:
            self.inverse[value] = set()
        self.inverse[value].add(item)
        super().__setitem__(item, value)

    def __delitem__(self, item):
        value = self[item]
        self.inverse[value].remove(item)
        if not self.inverse[value]:
            del self.inverse[value]
        super().__delitem__(item)

    def clear(self):
        super().clear()
        self.inverse.clear()


class CallbackDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_set = _empty
        self._on_new = _empty
        self._on_change = _empty
        self._on_del = _empty

    @property
    def on_set(self):
        return self._on_set

    @on_set.setter
    def on_set(self, value):
        num = required_num_of_args(inspect.signature(value))
        if num != 2:
            raise TypeError("on_set callback uses 2 args; received "
                            "{}".format(num))
        self._on_set = value

    @property
    def on_new(self):
        return self._on_new

    @on_new.setter
    def on_new(self, value):
        num = required_num_of_args(inspect.signature(value))
        if num != 2:
            raise TypeError("on_new callback uses 2 args; received "
                            "{}".format(num))
        self._on_new = value

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, value):
        num = required_num_of_args(inspect.signature(value))
        if num != 3:
            raise TypeError("on_change callback uses 3 args; received "
                            "{}".format(num))
        self._on_change = value

    @property
    def on_del(self):
        return self._on_del

    @on_del.setter
    def on_del(self, value):
        num = required_num_of_args(inspect.signature(value))
        if num != 1:
            raise TypeError("on_del callback uses 1 arg; received "
                            "{}".format(num))
        self._on_del = value

    def __setitem__(self, item, value):
        old_value = self.get(item, NULL)
        super().__setitem__(item, value)
        self.on_set(item, value)
        if old_value is not NULL:
            if old_value != value:
                self.on_change(item, old_value, value)
        else:
            self.on_new(item, value)

    def __delitem__(self, item):
        super().__delitem__(item)
        self.on_del(item)

    def clear(self):
        items = set(self.keys())
        super().clear()
        for item in items:
            self.on_del(item)


class CallbackPosDict(PosDict, CallbackDict):
    pass


class CallbackCellDict(CellDict, CallbackDict):
    pass


def required_num_of_args(sig):
    params = sig.parameters
    req = [p for p in params if params[p].default is params[p].empty]
    return len(req)


def _empty(*args):
    return args

