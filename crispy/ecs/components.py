import collections
import pickle
import weakref
from .entities import BaseEntity
from .eids import EIDRef


class ComponentManager(collections.OrderedDict):
    default_path = "components.pkl"

    def __init__(self):
        super().__init__()
        self.identity = object()
        self.eids = EIDRef()
        root = weakref.ref(self)

        class Entity(BaseEntity):
            def __init__(self, eid=None, **kwargs):
                if eid is None:
                    eid = root().eids.get_next()
                super().__init__(root(), eid, **kwargs)

        self.Entity = Entity

    def get_entity_component(self, entity, component):
        try:
            eid = entity.eid
        except AttributeError:
            eid = entity
        return self[component][eid]

    def set_entity_component(self, entity, component, value):
        try:
            eid = entity.eid
        except AttributeError:
            eid = entity
        self[component][eid] = value
        self.eids.increment(eid)

    def del_entity_component(self, entity, component):
        try:
            eid = entity.eid
        except AttributeError:
            eid = entity
        del self[component][eid]
        self.eids.decrement(eid)

    def clear(self, entity=None):
        if entity is None:
            for component in self:
                self[component].clear()
            self.eids.clear()
        else:
            self.clear_entity(entity)

    def clear_entity(self, entity):
        for component in self:
            try:
                self.del_entity_component(entity, component)
            except KeyError:
                continue

    def save(self, path=None):
        if not path:
            path = self.default_path
        save_dict = dict()
        for c in self:
            save_dict[c] = dict(self[c])
        with open(path, "wb") as f:
            pickle.dump(save_dict, f, pickle.HIGHEST_PROTOCOL)

    def load(self, path=None):
        if not path:
            path = self.default_path
        self.clear()
        with open(path, "rb") as f:
            file = pickle.load(f)
            for component in self:
                try:
                    comp_dict = file.pop(component)
                    for eid in comp_dict:
                        value = comp_dict[eid]
                        self.set_entity_component(eid, component, value)
                except KeyError:
                    # warning: file does not contain component
                    continue
                    # if file is not empty? warning: components not loaded

    def __eq__(self, other):
        try:
            return self.identity == other.identity
        except AttributeError:
            return False
