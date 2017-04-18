from .core import DieRoll


class CheckRoll(DieRoll):
    def __init__(self, roller=None):
        super().__init__(1, 20, roller=roller)
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
        return self.face >= self.crit_range

    def is_fumble(self):
        return self.face == 1

    def __str__(self):
        txt = super().__str__()
        txt += " ({0}+{1}) vs DC: {2}".format(self.face, self.bonus, self.dc)
        return txt


class CheckType:
    def __init__(self, bonus=None, dc=None, name=None, roller=None):
        if name is None:
            name = type(self).__name__
        self.name = name
        self.roller = roller
        if bonus is None:
            bonus = list()
        if dc is None:
            dc = list()
        self._bonus = dict(v.split(".") for v in bonus)
        self._dc = dict(v.split(".") for v in dc)

    def __call__(self, nt):
        kwargs = nt._asdict()
        req_keywords = set(self._bonus).union(self._dc)
        miss = {k for k in req_keywords if k not in kwargs}
        if miss:
            raise TypeError("{0}: missing keywords: {1}".format(self.name, miss))
        check = CheckRoll(roller=self.roller)
        for k in kwargs:
            if k in self._bonus:
                attr = self._bonus[k]
                subject = kwargs[k]
                bonus = getattr(subject, attr)
                check.bonus += bonus
            if k in self._dc:
                attr = self._dc[k]
                subject = kwargs[k]
                dc = getattr(subject, attr)
                check.dc += dc
        return check


