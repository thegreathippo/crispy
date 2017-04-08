"""
TODO:
    * Fix entities. ATM, we have a hidden reference (via the root) that ought to be cleaned up, somehow. Probably by
      dropping the entity class into the root class and using weakref.

"""
from .processes import ProcessManager
from .utils import NULL, required_num_of_args
from .callbackdicts import CallbackDict
from .customdicts import InvertibleDict, ReversibleDict
