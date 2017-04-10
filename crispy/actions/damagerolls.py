from .dicerolls import DicePool


class DamageRoll(DicePool):
    def __str__(self):
        return super().__str__()


class DamageType:
    def __init__(self, source=None):
        if source is None:
            source = list()
        self._source = dict(v.split(".") for v in source)

    def __call__(self, subjects):
        damageroll = DamageRoll()
        for field in subjects._fields:
            if field in self._source:
                attr = self._source[field]
                dieroll = getattr(getattr(subjects, field), attr)
                damageroll.add(*dieroll)
        return damageroll
