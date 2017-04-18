import pickle
from . import components
from . import entities
from . import processes

EidRef = entities.EidRef
entity_cls = entities.entity_cls
PATH = 'components.pkl'


class System:
    def __init__(self, *args, **kwargs):
        self.components = components.OuterDict(*args, **kwargs)
        self.Entity = entity_cls("Entity", self.components)
        self.eids = EidRef()
        self.processes = processes.ProcessManager(self.components, self.get_entity)

        def increment(eid, *args):
            self.eids.increment(eid)

        def decrement(eid, *args):
            self.eids.decrement(eid)

        for value in self.components.values():
            value.bind_new(increment)
            value.bind_del(decrement)

    def new_entity(self, **kwargs):
        eid = self.eids.get_next()
        return self.Entity(eid, **kwargs)

    def get_entity(self, eid):
        return self.Entity(eid)

    def bind_new(self, comp_name, func):
        def binder(eid, value):
            entity = self.get_entity(eid)
            return func(entity, value)

        self.components[comp_name].bind_new(binder)

    def bind_change(self, comp_name, func):
        def binder(eid, old_val, new_val):
            entity = self.get_entity(eid)
            return func(entity, old_val, new_val)

        self.components[comp_name].bind_change(binder)

    def bind_del(self, comp_name, func):
        def binder(eid):
            entity = self.get_entity(eid)
            return func(entity)

        self.components[comp_name].bind_del(binder)

    def clear(self):
        for eid in list(self.eids):
            entity = self.get_entity(eid)
            self.clear_entity(entity)

    def clear_entity(self, entity):
        for comp_name in self.components:
            try:
                delattr(entity, comp_name)
            except AttributeError:
                continue

    def save(self, path=None):
        if not path:
            path = PATH
        save_dict = dict()
        for k, v in self.components.items():
            save_dict[k] = dict(v)
        with open(path, "wb") as f:
            pickle.dump(save_dict, f, pickle.HIGHEST_PROTOCOL)

    def load(self, path=None):
        if not path:
            path = PATH
        self.clear()
        with open(path, "rb") as f:
            file = pickle.load(f)
            for name in self.components:
                try:
                    comp_dict = file.pop(name)
                    for eid, value in comp_dict.items():
                        self.components[name][eid] = value
                except KeyError:
                    # file does not contain component
                    continue
            if file:
                # file not empty? component(s) not loaded
                pass

    def __getitem__(self, item):
        return self.components[item]

    def __iter__(self):
        for eid in self.eids:
            yield self.get_entity(eid)

    def __len__(self):
        return len(self.eids)
