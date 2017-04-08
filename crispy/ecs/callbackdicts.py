from .utils import NULL, required_num_of_args


class CallbackDict(dict):
    def __init__(self, root):
        super().__init__()
        self._on_new = Callbacks(root.Entity)
        self._on_change = Callbacks(root.Entity)
        self._on_del = Callbacks(root.Entity)

    def bind_new(self, callback):
        num = required_num_of_args(callback)
        if num != 2:
            raise TypeError("bind_new callback requires 2 args, "
                            "received {}".format(num))
        self._on_new.append(callback)
        for k, v in self.items():
            self._on_new(k, v)

    def bind_change(self, callback):
        num = required_num_of_args(callback)
        if num != 3:
            raise TypeError("bind_change callback requires 3 args, "
                            "received {}".format(num))
        self._on_change.append(callback)

    def bind_del(self, callback):
        num = required_num_of_args(callback)
        if num != 1:
            raise TypeError("bind_del callback requires 1 arg, "
                            "received {}".format(num))
        self._on_del.append(callback)

    def clear(self):
        old_keys = list(self.keys())
        super().clear()
        for key in old_keys:
            self._on_del(key)

    def update(self, other=None, **kwargs):
        o_dict = dict(self)
        if other:
            super().update(other, **kwargs)
        else:
            super().update(**kwargs)
        for k, v in self.items():
            if k not in o_dict:
                self._on_new(k, self[k])
            elif v != o_dict[k]:
                self._on_change(k, o_dict[k], self[k])

    def setdefault(self, key, default=None):
        old_val = self.get(key, NULL)
        ret = super().setdefault(key, default)
        if old_val is NULL:
            self._on_new(key, self[key])
        return ret

    def popitem(self):
        ret = super().popitem()
        self._on_del(ret[0])
        return ret

    def pop(self, key, default=NULL):
        if default is NULL:
            ret = super().pop(key)
        else:
            ret = super().pop(key, default)
        self._on_del(key)
        return ret

    def clear_bindings(self):
        self._on_new.clear()
        self._on_change.clear()
        self._on_del.clear()

    def __setitem__(self, item, value):
        old_val = self.get(item, NULL)
        super().__setitem__(item, value)
        if old_val is NULL:
            self._on_new(item, value)
        elif old_val != value:
            self._on_change(item, old_val, value)

    def __delitem__(self, item):
        super().__delitem__(item)
        self._on_del(item)


class Callbacks(list):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def __call__(self, *args):
        for obj in self:
            obj(self.f(args[0]), *args[1:])
