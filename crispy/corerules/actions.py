from .bases.localevents import LocalEvent
from .bases.dice import Check, DicePool


class EventCheck(LocalEvent):
    bonus = dict()
    dc = dict()

    def __init__(self, **kwargs):
        bonus = 0
        for name in self.bonus:
            bonus += getattr(kwargs[name], self.bonus[name])
        dc = 10
        for name in self.dc:
            dc += getattr(kwargs[name], self.dc[name])
        self.check = Check(bonus=bonus, dc=dc)

    def finalize(self):
        check = self.check
        if check.is_critical():
            self.on_critical()
        elif check.is_fumble():
            self.on_fumble()
        elif check.is_success():
            self.on_success()
        else:
            self.on_failure()

    def on_success(self):
        pass

    def on_failure(self):
        pass

    def on_critical(self):
        self.on_success()

    def on_fumble(self):
        self.on_failure()


class EventAttack(EventCheck):
    die = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dicepool = DicePool()
        die = list()
        for name in self.die:
            die.append(getattr(kwargs[name], self.die[name]))
        for d in die:
            self.dicepool.add_die(d)

