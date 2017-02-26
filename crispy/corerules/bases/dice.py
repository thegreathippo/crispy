import random


class Check:
    def __init__(self, bonus=0, dc=10, crit_range=20, vantage=0):
        self.bonus = bonus
        self.dc = dc
        self.crit_range = crit_range
        self.vantage = vantage
        roll = [random.randint(1, 20), random.randint(1, 20)]
        self._first = roll[0]
        roll.sort()
        self._low = roll[0]
        self._high = roll[1]

    @property
    def roll(self):
        if not self.vantage:
            return self._first
        elif self.vantage > 0:
            return self._high
        else:
            return self._low

    def get_total(self):
        return self.roll + self.bonus

    def is_success(self):
        return (self.get_total() >= self.dc or
                self.is_critical())

    def is_failure(self):
        if self.is_critical():
            return False
        return (self.get_total() < self.dc or
                self.is_fumble())

    def is_critical(self):
        return (self.roll >= self.crit_range)

    def is_fumble(self):
        return (self.roll == 1)


class DicePool(dict):
    def __init__(self, die=None):
        super().__init__()
        self.base = None
        if die:
            self.add_die(die)

    def add_die(self, arg):
        try:
            len(arg)
        except TypeError:
            return self._add_die(None, 0, 0, arg)
        if len(arg) == 1:
            return self._add_die(None, 0, 0, arg[0])
        if len(arg) == 2:
            if isinstance(arg[0], int):
                return self._add_die(None, arg[0], arg[1], 0)
            else:
                return self._add_die(arg[0], 0, 0, arg[1])
        elif len(arg) == 3:
            if isinstance(arg[0], int):
                return self._add_die(None, arg[0], arg[1], arg[2])
            else:
                return self._add_die(arg[0], arg[1], arg[2], 0)
        else:
            return self._add_die(arg[0], arg[1], arg[2], arg[3])

    def _add_die(self, category, num, face, bonus):
        if category not in self:
            if not self:
                self.base = category
            self[category] = list()
        die = Die(num, face, bonus)
        self[category].append(die)

    def get_roll(self):
        roll = Roll()
        for category in self:
            roll[category] = 0
            for die in self[category]:
                roll[category] += die.roll()
        return roll


class Roll(dict):
    def get_total(self):
        val = 0
        for category in self:
            val += self[category]
        return val


class Die:
    def __init__(self, num, face, bonus=0):
        self.num = num
        self.face = face
        self.bonus = bonus

    def roll(self):
        val = 0
        for i in range(0, self.num):
            val += random.randint(1, self.face)
        val += self.bonus
        return val

    def __repr__(self):
        txt = ""
        if self.num:
            txt += "{0}d{1}".format(self.num, self.face)
        if self.bonus:
            txt += "+{0}".format(self.bonus)
        return txt