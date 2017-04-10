from collections import namedtuple

ENERGY = "energy"

_action = dict()
_subjects = dict()
_bases = dict()
_after = dict()
_before = dict()
_abstracts = list()


def abstract(cls):
    _abstracts.append(cls)
    return cls


Rule = namedtuple("Rule", ["func", "priority"])


class BehaviorBase:
    actions = _action
    subjects = _subjects


class ActionType(type):
    def __new__(meta, name, bases, namespace):
        cls = super().__new__(meta, name, bases, namespace)
        _action[name] = cls
        _subjects[cls] = namedtuple("Subjects", getattr(cls, "subjects"))
        _bases[cls] = [c for c in reversed(cls.mro()) if c != object]
        _after[cls] = list()
        _before[cls] = list()
        return cls

    def __call__(cls, *args, **kwargs):
        if cls in _abstracts:
            raise Exception("{} is abstract action".format(cls))
        instance = super().__call__(*args, **kwargs)
        instance.before()
        for base in _bases[cls]:
            for rule in _before[base]:
                rule.func(instance)
        for base in _bases[cls]:
            subjects = instance.subjects._asdict()
            for label, obj in subjects.items():
                try:
                    behavior = obj.behavior
                except AttributeError:
                    continue
                behavior(base, label, instance)
        for base in _bases[cls]:
            for rule in _after[base]:
                rule.func(instance)
        instance.after()
        agent = instance.subjects[0]
        try:
            agent.energy -= instance.cost
        except AttributeError:
            pass
        del instance.subjects
        return instance


@abstract
class Action(metaclass=ActionType):
    subjects = ["agent"]
    check_type = None
    damage_type = None
    cost = 0

    def __init__(self, *args, **kwargs):
        self.subjects = _subjects[type(self)](*args, **kwargs)
        if self.check_type:
            self.check = self.check_type(self.subjects)
        if self.damage_type:
            self.damage = self.damage_type(self.subjects)

    def after(self):
        pass

    def before(self):
        pass

    @classmethod
    def bind_after(cls, func, priority=0):
        rule = Rule(func, priority)
        _after[cls].append(rule)
        _after[cls].sort(key=lambda r: r.priority)

    @classmethod
    def bind_before(cls, func, priority=0):
        rule = Rule(func, priority)
        _before[cls].append(rule)
        _before[cls].sort(key=lambda r: r.priority)


