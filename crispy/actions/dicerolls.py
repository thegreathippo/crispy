import random
import weakref
import collections

namedtuple = collections.namedtuple
randint = random.randint


def roller(self, low, high):
    return [randint(low, high), randint(low, high)]


class DieRoll:
    roller = roller

    def __init__(self, *args):
        self.die = _get_die(args)
        self.roll = _get_roll(self.die, self.roller)
        self.bonus = self.die.bonus
        self.vantage = 0

    def get(self, vantage=None):
        if vantage is None:
            return self.value
        else:
            if vantage == 0:
                return self.roll.first + self.bonus
            elif vantage > 0:
                return self.roll.high + self.bonus
            else:
                return self.roll.low + self.bonus

    @property
    def face(self):
        if not self.vantage:
            return self.roll.first
        elif self.vantage > 0:
            return self.roll.high
        else:
            return self.roll.low

    @property
    def value(self):
        return self.face + self.bonus

    def __repr__(self):
        n, f, b = self.die.number, self.die.face, self.bonus
        if n and f and b:
            return "{0}d{1}+{2}".format(n, f, b)
        elif n and f:
            return "{0}d{1}".format(n, f)
        elif b:
            return "+{0}".format(b)


class Dice:
    # Add a bonus field? Adds to value?
    roller = roller

    def __init__(self, *args):
        super().__init__()
        self.vantage = 0
        self._dierolls = list()
        dice = weakref.ref(self)

        class _DieRoll(DieRoll):
            def unbind(self):
                dice().remove(self)
                # Once unbound, it's just a DieRoll.
                self.__class__ = DieRoll

            @property
            def roller(self):
                return dice().roller

        self._DieRoll = _DieRoll
        if args:
            self.add(*args)

    def add(self, *args):
        dieroll = self._DieRoll(*args)
        self._dierolls.append(dieroll)
        return dieroll

    def remove(self, dieroll):
        self._dierolls.remove(dieroll)

    def get(self, vantage=None):
        if vantage is None:
            return self.value
        else:
            return sum([r.get(vantage) for r in self._dierolls])

    def clear(self):
        self._dierolls.clear()

    @property
    def value(self):
        return self.get(vantage=self.vantage)

    def __str__(self):
        return "{0}".format(super().__repr__())

    def __getitem__(self, item):
        return self._dierolls[item]

    def __eq__(self, other):
        return self._dierolls == other

    def __repr__(self):
        return str(self._dierolls)


class DicePool:
    roller = roller

    def __init__(self, dice_type=None, *args):
        super().__init__()
        self.vantage = None
        self._die = dict()
        self._dice = dict()
        dicepool = weakref.ref(self)

        class _Dice(Dice):

            def remove_dieroll(self, dieroll):
                super().remove(dieroll)
                dp = dicepool()
                dice_type = dp._die[dieroll]
                if not dp[dice_type]:
                    del dp[dice_type]
                del dp._die[dieroll]

            @property
            def roller(self):
                return dicepool().roller

        self._Dice = _Dice
        if args:
            self.add(dice_type, *args)

    def add(self, dice_type=None, *args):
        if dice_type not in self:
            self[dice_type] = self._Dice()
        dieroll = self[dice_type].add(*args)
        self._die[dieroll] = dice_type
        return dieroll

    def remove(self, dieroll):
        dice_type = self._die[dieroll]
        self[dice_type].remove_die(dieroll)

    def get(self):
        result = _DicePoolDict()
        for dice_type in self:
            if self.vantage:
                result[dice_type] = self[dice_type].get(self.vantage)
            else:
                result[dice_type] = self[dice_type].value
        return result

    def clear(self):
        self._dice.clear()
        self._die.clear()

    def __getitem__(self, item):
        return self._dice[item]

    def __setitem__(self, item, value):
        self._dice[item] = value

    def __delitem__(self, item):
        del self._dice[item]

    def __contains__(self, item):
        return item in self._dice

    def __iter__(self):
        return iter(self._dice)

    def __eq__(self, other):
        return self._dice == other

    def __repr__(self):
        return "{0}{1}".format(type(self).__name__, self._dice)


class _DicePoolDict(dict):
    def total(self):
        result = 0
        for val in self.values():
            result += val
        return result


Die = namedtuple("Die", ["number", "face", "bonus"])


def _get_die(args):
    n, f, b = 0, 0, 0
    try:
        n, f, b = args
    except ValueError:
        try:
            n, f = args
        except ValueError:
            b = args[0]
    return Die(n, f, b)


Roll = namedtuple("Roll", ["first", "high", "low"])


def _get_roll(die, roller=roller):
    first, high, low = 0, 0, 0
    for i in range(0, die.number):
        roll = roller(1, die.face)
        first += roll[0]
        roll.sort()
        high += roll[1]
        low += roll[0]
    return Roll(first, high, low)