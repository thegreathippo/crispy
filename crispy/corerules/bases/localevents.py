BEHAVIOR = "behaviors"


class LocalEventType(type):
    def __call__(cls, *args, **kwargs):
        missing = set(cls.subjects).difference(kwargs)
        if missing:
            raise Exception("{0} did not receive all subjects: {1}".format(cls, missing))
        instance = super().__call__(*args, **kwargs)
        subjects = {k: v for (k, v) in kwargs.items() if k in cls.subjects}
        if any(hasattr(instance, s) for s in subjects):
            raise Exception("{0} initialized with attributes: {1}".format(cls, set(subjects)))
        instance.__dict__.update(subjects)
        for base in reversed(cls.mro()):
            instance.apply_pre_rules(base)
        for base in reversed(cls.mro()):
            if base is object: continue
            for name in cls.subjects:
                subject = subjects[name]
                try:
                    behaviors = getattr(subject, BEHAVIOR)
                except AttributeError:
                    continue
                behavior = behaviors.get(base.__name__, None)
                if behavior:
                    scripts = behavior.get(name, None)
                    if scripts:
                        for script in scripts:
                            script(instance)
        for base in reversed(cls.mro()):
            instance.apply_post_rules(base)
        instance.finalize()
        for s in subjects:
            delattr(instance, s)
        return instance


class LocalEvent(metaclass=LocalEventType):
    subjects = ["agent"]

    def finalize(self):
        pass

    def apply_pre_rules(self, cls):
        if "pre_rules" in cls.__dict__:
            for rule in cls.pre_rules:
                rule(self)

    def apply_post_rules(self, cls):
        if "post_rules" in cls.__dict__:
            for rule in cls.post_rules:
                rule(self)

    @classmethod
    def add_post_rule(cls, rule):
        if "post_rules" not in cls.__dict__:
            cls.post_rules = list()
        cls.post_rules.append(rule)

    @classmethod
    def add_pre_rule(cls, rule):
        if "pre_rules" not in cls.__dict__:
            cls.pre_rules = list()
        cls.pre_rules.append(rule)

