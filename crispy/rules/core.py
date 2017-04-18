import weakref
import collections
from .bindings import Binding

_event = set()
_bases = dict()
_after = dict()
_before = dict()
_subjects = dict()


class EventType(type):
    def __new__(meta, name, bases, namespace):
        cls = super().__new__(meta, name, bases, namespace)
        if name in _event:
            raise NameError("{} is already an EventType".format(name))
        _event.add(name)
        if not name.startswith("_"):
            _bases[cls] = [c for c in reversed(cls.mro()) if c != object]
            _after[cls], _before[cls] = list(), list()
        _subjects[cls] = collections.namedtuple("Subjects", cls.subjects)
        return cls

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.before()
        for base in _bases[cls]:
            for rule in _before[base]:
                rule.func(instance)
        for base in _bases[cls]:
            for label in base.subjects:
                subject = getattr(instance, label)
                try:
                    behavior = subject.behavior
                except AttributeError:
                    continue
                behavior(base, label, instance)
        for base in _bases[cls]:
            for rule in _after[base]:
                rule.func(instance)
        instance.after()
        return instance


class SubjectProperty:
    def __init__(self, label):
        self._label = "_" + label

    def __get__(self, instance, cls):
        try:
            return getattr(instance, self._label)()
        except AttributeError:
            return None

    def __set__(self, instance, value):
        setattr(instance, self._label, weakref.ref(value))

    def __delete__(self, instance):
        delattr(instance, self._label)


class Event(metaclass=EventType):
    subjects = ("agent",)
    agent = SubjectProperty("agent")

    def __init__(self, *args):
        if len(args) != len(self.subjects):
            raise TypeError("{0} requires {1} args, received {2}".format(type(self).__name__,
                                                                         len(self.subjects), len(args)))
        for i, label in enumerate(self.subjects):
            setattr(self, label, args[i])

    def get_subjects(self):
        subjects = list()
        for k in self.subjects:
            subjects.append(getattr(self, k))
        cls = _subjects[type(self)]
        return cls(*subjects)

    def before(self):
        pass

    def after(self):
        pass

    @classmethod
    def bind_after(cls, func, priority=0):
        rule = Binding(func, priority)
        after = _after[cls]
        after.append(rule)
        after.sort(key=lambda r: r.priority)
        rule.add_unbinder(after.remove, rule)
        return rule

    @classmethod
    def bind_before(cls, func, priority=0):
        rule = Binding(func, priority)
        before = _before[cls]
        before.append(rule)
        before.sort(key=lambda r: r.priority)
        rule.add_unbinder(before.remove, rule)
        return rule

