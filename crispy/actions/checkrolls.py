from .dicerolls import DieRoll


class Check(DieRoll):
    def __init__(self):
        super().__init__(1, 20)
        self.crit_range = 20
        self.dc = 10

    def is_success(self):
        return (self.value >= self.dc or
                self.is_critical())

    def is_failure(self):
        if self.is_critical():
            return False
        return (self.value < self.dc or
                self.is_fumble())

    def is_critical(self):
        return (self.face >= self.crit_range)

    def is_fumble(self):
        return (self.face == 1)

    def __str__(self):
        txt = super().__str__()
        txt += " ({0}+{1}) vs DC: {2}".format(self.face, self.bonus, self.dc)
        return txt


class CheckType:
    def __init__(self, bonus=None, dc=None):
        if bonus is None:
            bonus = list()
        if dc is None:
            dc = list()
        self._bonus = dict(v.split(".") for v in bonus)
        self._dc = dict(v.split(".") for v in dc)

    def __call__(self, subjects):
        check = Check()
        for field in subjects._fields:
            if field in self._bonus:
                attr = self._bonus[field]
                bonus = getattr(getattr(subjects, field), attr)
                check.bonus += bonus
            if field in self._dc:
                attr = self._dc[field]
                dc = getattr(getattr(subjects, field), attr)
                check.dc += dc
        return check

