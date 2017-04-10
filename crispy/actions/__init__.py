"""
TODO:
    * Make an enhanced namedtuple class for use in actions?
    * Better documentation (obviously)
    * Fix BoundDice/BoundDie (no need; just shove 'unbind' in as an attribute). Test before doing this.
    * Going to need to raise an exception if you try to create action classes with identical names
    * Determine if 'before' and 'after' functions are actually necessary.
    * Try to clarify use of CheckType and DamageType as a class variable re: as an instance attribute
    * Consider making 'utils.py' just a module we copy into all our packages with utilities we keep needing,
        rather than a global or a different module in each package.
    * Pickling for Behavior objects? How are they saved? Will need to do extensive testing D:

"""
from . import movement
from . import attacks
from . import damages
