"""Contains the BaseEntity class; this is the base class for
all entity objects.
"""


class BaseEntity:
    def __init__(self, *args, **kwargs):
        """Initialize the BaseEntity class instance.

        ARGUMENTS:
          args: A 2-value tuple containing an instance of the ComponentManager
            class (or any class that inherits from it) and an eid (an integer
            representing this entity's identity).
          kwargs: Keyword arguments that will be assigned as attributes
            (components) to this entity.

        EXCEPTIONS:
          ValueError: Raised if *args is not a 2D sequence.
        """
        # TODO:
        #   * Error-check root? Ensure it has correct methods?
        root, eid = args
        self.__dict__["root"] = root
        self.eid = eid
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __getattr__(self, attr):
        try:
            return self.root.get_entity_component(self, attr)
        except KeyError:
            return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr not in self.root:
            super().__setattr__(attr, value)
        else:
            self.root.set_entity_component(self, attr, value)

    def __delattr__(self, attr):
        try:
            super().__delattr__(attr)
        except AttributeError:
            self.root.del_entity_component(self, attr)

    def __eq__(self, other):
        try:
            return (other.eid, other.root) == (self.eid, self.root)
        except AttributeError:
            return False

