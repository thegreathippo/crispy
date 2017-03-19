NULL = object()


class InverseDict(dict):
    def __init__(self):
        super().__init__()
        self.inverse = dict()

    def __setitem__(self, item, value):
        old_value = self.get(item, NULL)
        if not old_value is NULL:
            del self.inverse[old_value]
        super().__setitem__(item, value)
        self.inverse[value] = item

    def __delitem__(self, item):
        value = self[item]
        super().__delitem__(item)
        del self.inverse[value]


class ReverseDict(dict):
    def __init__(self):
        super().__init__()
        self.reverse = dict()

    def __setitem__(self, item, value):
        old_value = self.get(item, NULL)
        if not old_value is NULL:
            self.reverse[old_value].remove(item)
            if not self.reverse[old_value]:
                del self.reverse[old_value]
        if value not in self.reverse:
            self.reverse[value] = set()
        self.reverse[value].add(item)
        super().__setitem__(item, value)

    def __delitem__(self, item):
        value = self[item]
        super().__delitem__(item)
        self.reverse[value].remove(item)
        if not self.reverse[value]:
            del self.reverse[value]


class CallbackDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_add = list()
        self._on_change = list()
        self._on_remove = list()

    def on_add(self, callback):
        self._on_add.append(callback)

    def on_change(self, callback):
        self._on_change.append(callback)

    def on_remove(self, callback):
        self._on_remove.append(callback)

    def __setitem__(self, item, value):
        old_value = self.get(item, NULL)
        super().__setitem__(item, value)
        if not old_value is NULL:
            for callback in self._on_change:
                callback(item, old_value, value)
        else:
            for callback in self._on_add:
                callback(item, value)

    def __delitem__(self, item):
        super().__delitem__(item)
        for callback in self._on_remove:
            callback(item)
