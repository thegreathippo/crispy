from .core import DicePool


class DamageRoll(DicePool):
    def __str__(self):
        return super().__str__()


class DamageType:
    def __init__(self, source=None, name=None, roller=None):
        if name is None:
            name = type(self).__name__
        self.name = name
        self.roller = roller
        if source is None:
            source = list()
        self._source = dict(v.split(".") for v in source)

    def __call__(self, nt):
        kwargs = nt._asdict()
        req_keywords = set(self._source)
        miss = {k for k in req_keywords if k not in kwargs}
        if miss:
            raise TypeError("{0}: missing keywords: {1}".format(self.name, miss))
        damageroll = DamageRoll(roller=self.roller)
        for k in kwargs:
            if k in self._source:
                attr = self._source[k]
                subject = kwargs[k]
                dieroll = getattr(subject, attr)
                damageroll.add(*dieroll)
        return damageroll

