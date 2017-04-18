from .bindings import Binding


class Behavior:
    def __init__(self):
        self.bindings = dict()

    def __call__(self, cls, label, instance):
        clsname = cls.__name__
        if clsname in self.bindings:
            if label in self.bindings[clsname]:
                for rule in self.bindings[clsname][label]:
                    rule(instance)

    def bind(self, clsname, label, func, priority=0):
        if clsname not in self.bindings:
            self.bindings[clsname] = dict()
        if label not in self.bindings[clsname]:
            self.bindings[clsname][label] = list()
        rules = self.bindings[clsname][label]
        rule = Binding(func, priority)
        rules.append(rule)
        rules.sort(key=lambda x: x.priority)
        rule.add_unbinder(rules.remove, rule)
        return rule
