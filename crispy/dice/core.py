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


class Dice(dict):

  def __init__(self, die=None):
    self.roll = dict()
    if die:
      self.add_die(die)

  def add_die(self, arg):
    a = arg[0]
    if not isinstance(a, int):
      category = a
      rest = arg[1:]
    else:
      category = None
      rest = arg
    self._set_base(category)
    if len(rest) == 1:
      num, face, bonus = 0, 0, rest[0]
    elif len(rest) == 2:
      num, face, bonus = rest[0], rest[1], 0
    else:
      num, face, bonus = rest
    if category not in self:
      self[category] = list()
      self.roll[category] = 0
    die = Die(num, face, bonus)
    self[category].append(die)
    self.roll[category] += die.roll()

  def add_base_die(self, arg):
    new_arg = [self.base, *arg]
    self.add_die(new_arg)

  @property
  def base(self):
    try:
      return self._base
    except AttributeError:
      return None

  def _set_base(self, val):
    if not hasattr(self, "_base"):
      self._base = val

  def get_total(self):
    val = 0
    for category in self.roll:
      val += self.roll[category]
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
