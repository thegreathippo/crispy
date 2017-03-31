"""Contains the ComponentManager class; the base for the ProcessManager class.

The ComponentManager class assumes responsibility for maintaining all components
(entity attributes) contained in a system. It provides methods to
'hook' into an entity's attribute assignments (via on_new, on_change, and
on_del), pickle all components, load pickled components, and clear
all components.

"""
import collections
import pickle
import inspect
from .entities import BaseEntity

# Used in place of None.
NULL = object()


class _Callback:
    def __init__(self, func, send_eid):
        self.func = func
        self.send_eid = send_eid

    def __call__(self, *args):
        if self.send_eid:
            e, args = args[0].eid, args[1:]
        else:
            e, args = args[0], args[1:]
        self.func(e, *args)


Callback = collections.namedtuple("Callback", ["send_eid", "func"])


class ComponentManager(collections.OrderedDict):
    reserved_eids = 2
    default_save_path = "components.pkl"
    r_id = 0
    entity_cls = BaseEntity

    def __init__(self):
        """Initialize the ComponentManager class instance.

        CLASS ATTRIBUTES:
          reserved_eids (int): The number of 'reserved' eid #'s (entities
            which are presumed to always exist, and should therefore not
            be overwritten)
          default_save_path (str): The path this will use for saving and
            loading if no path is provided.
          r_id (int): The instance's ID value. Assigned to each instance, then
            increased by one on the class. Used as part of an entity
            instance's __eq__ and __hash__.
          entity_cls (class): The base class used to generate entities.

        ATTRIBUTES:
          r_id (int): The instance's ID value. Used as part of an entity
            instance's equality comparison and for its hash value.
          eid_count (int): The counter used to generate eids.
          _on_new (dict): A mapping of components (strings) to a list of
            callbacks that will activate whenever an entity gains a value
            for this component (and did not have a value prior).
          _on_change (dict): A mapping of components (strings) to a list
            of callbacks that will activate whenever an entity changes a
            value for this component.
          _on_del (dict): A mapping of components (strings) to a list of
            callbacks that will activate whenever an entity deletes a
            component.
          """
        super().__init__()
        self.r_id = self.r_id
        type(self).r_id += 1
        self.eid_count = self.reserved_eids
        self._on_new = dict()
        self._on_change = dict()
        self._on_del = dict()

    def bind_new(self, component, callback, send_eid=True):
        """Associate a callback with a component. This callback will
        be activated whenever an entity assigns a value to this
        component (and no value was assigned prior).

        The callback must accept two arguments; the entity/eid and
        the value this entity has assigned to the component.

        ARGUMENTS:
          component (str): The component that the callback will be
            associated with.
          callback: The callback in question.
          send_eid (boolean): If True, send the entity's eid to the
            callback; if False, send the entity. Defaults to True.

        EXCEPTIONS:
          TypeError: Raised when the callback is a non-callable, or
            when the callback does not accept the correct number of
            arguments (two).

        NOTE:
          The distinction between a callback that sends an entity --
          versus an entity's eid -- is an important one. Sending an eid
          carries no intrinsic risk of a recursive loop, because you
          cannot modify the entity's attributes (and therefore cannot
          cause another callback). Also, since they are just integers,
          relying on eids prevents memory leaks and unexpected
          object mutation. Whenever it's reasonably possible, you should
          send an eid instead of an entity.
        """
        num = required_num_of_args(callback)
        if num != 2:
            raise TypeError("on_new requires 2 args; has {}".format(num))
        if component not in self._on_new:
            self._on_new[component] = list()
        self._on_new[component].append(_Callback(callback, send_eid))

    def bind_change(self, component, callback, send_eid=True):
        """Associate a callback with a component. This callback will
        be activated whenever an entity changes a value for this
        component.

        The callback must accept three arguments; the entity/eid, the
        original value, and the new value.

        ARGUMENTS:
          component (str): The component that the callback will be
            associated with.
          callback: The callback in question.
          send_eid (boolean): If True, send the entity's eid to the
            callback; if False, send the entity. Defaults to True.

        EXCEPTIONS:
          TypeError: Raised when the callback is a non-callable, or
            when the callback does not accept the correct number of
            arguments (three).

        NOTE:
          The distinction between a callback that sends an entity --
          versus an entity's eid -- is an important one. Sending an eid
          carries no intrinsic risk of a recursive loop, because you
          cannot modify the entity's attributes (and therefore cannot
          cause another callback). Also, since they are just integers,
          relying on eids prevents memory leaks and unexpected
          object mutation. Whenever it's reasonably possible, you should
          send an eid instead of an entity.
        """
        num = required_num_of_args(callback)
        if num != 3:
            raise TypeError("on_change requires 3 args; has {}".format(num))
        if component not in self._on_change:
            self._on_change[component] = list()
        self._on_change[component].append(_Callback(callback, send_eid))

    def bind_del(self, component, callback, send_eid=True):
        """Associate a callback with a component. This callback will
        be activated whenever an entity deletes a value for this
        component.

        The callback must accept one argument; the entity/eid.

        ARGUMENTS:
          component (str): The component that the callback will be
            associated with.
          callback: The callback in question.
          send_eid (boolean): If True, send the entity's eid to the
            callback; if False, send the entity. Defaults to True.

        EXCEPTIONS:
          TypeError: Raised when the callback is a non-callable, or
            when the callback does not accept the correct number of
            arguments (one).

        NOTE:
          The distinction between a callback that sends an entity --
          versus an entity's eid -- is an important one. Sending an eid
          carries no intrinsic risk of a recursive loop, because you
          cannot modify the entity's attributes (and therefore cannot
          cause another callback). Also, since they are just integers,
          relying on eids prevents memory leaks and unexpected
          object mutation. Whenever it's reasonably possible, you should
          send an eid instead of an entity.
        """
        num = required_num_of_args(callback)
        if num != 1:
            raise TypeError("on_del requires 1 arg; has {}".format(num))
        if component not in self._on_del:
            self._on_del[component] = list()
        self._on_del[component].append(_Callback(callback, send_eid))

    def get_entity(self, eid=None, **kwargs):
        """Return an entity; either one associated with the provided
        eid, or a new entity associated with a new eid.

        ARGUMENTS:
          eid (int): An integer that serves as the entity's eid. If
            no eid is provided, a new eid is generated.
          kwargs: Component-values that are assigned to the entity.
        """
        if eid is None:
            eid = self.eid_count + 1
            self.eid_count += 1
        return self.entity_cls(self, eid, **kwargs)

    def get_entity_component(self, entity, component):
        """Return the value associated with an entity's component."""
        return self[component][entity.eid]

    def set_entity_component(self, entity, component, value):
        """Set a value on an entity's component."""
        old_val = self[component].get(entity.eid, NULL)
        self[component][entity.eid] = value
        if old_val is NULL:
            for callback in self._on_new.get(component, list()):
                callback(entity, self[component][entity.eid])
        elif old_val != value:
            for callback in self._on_change.get(component, list()):
                callback(entity, old_val, self[component][entity.eid])

    def del_entity_component(self, entity, component):
        """Delete an entity's component."""
        del self[component][entity.eid]
        for callback in self._on_del.get(component, list()):
            callback(entity)

    def clear(self, entity=None):
        """Clear an entity's components or clear all entities of
        their components. In both cases, all relevant on_del callbacks
        will be triggered.

        ARGUMENTS:
          entity: The entity to be cleared. If no entity is provided,
            all entities will be cleared.
        """
        if entity is not None:
            self.clear_entity(entity)
        else:
            for component in self:
                while self[component]:
                    try:
                        eid = self[component].popitem()[0]
                    except KeyError:
                        continue
                    for callback in self._on_del.get(component, list()):
                        callback(self.get_entity(eid))
            self.eid_count = self.reserved_eids

    def clear_entity(self, entity):
        """Clear an entity's components."""
        for component in self:
            try:
                self.del_entity_component(entity, component)
            except KeyError:
                continue

    def save(self, path=None):
        """Save the contents of this instance to the provided path
        through the pickle module.

        ARGUMENTS:
          path: The path for the file to be saved to. Defaults to
            the class' default_save_path attribute.
        """
        if not path:
            path = self.default_save_path
        save_dict = dict()
        for c in self:
            save_dict[c] = dict(self[c])
        with open(path, "wb") as f:
            pickle.dump(save_dict, f, pickle.HIGHEST_PROTOCOL)

    def load(self, path=None):
        """Clear the contents of this instance's components and load
        new values into its components from the file at the provided
        path.

        ARGUMENTS:
          path: A path to the file to be loaded.

        """
        if not path:
            path = self.default_save_path
        self.clear()
        eid_translation = get_eid_translation(self.reserved_eids)
        eid_count = self.reserved_eids
        with open(path, "rb") as f:
            data = pickle.load(f)
            for component in self:
                for eid in data[component]:
                    if eid not in eid_translation:
                        eid_translation[eid] = eid_count + 1
                        eid_count += 1
                    t_eid = eid_translation[eid]
                    entity = self.get_entity(t_eid)
                    value = data[component][eid]
                    self.set_entity_component(entity, component, value)
        self.eid_count = eid_count


def get_eid_translation(reserved_eids):
    result = dict()
    for eid in range(0, reserved_eids + 1):
        result[eid] = eid
    return result


def required_num_of_args(func):
    """Return the number of arguments this function requires."""
    sig = inspect.signature(func)
    params = sig.parameters
    req = [p for p in params if params[p].default is params[p].empty]
    return len(req)


