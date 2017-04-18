class Binding:
    def __init__(self, func, priority=0):
        self.func = func
        self.priority = priority
        self._unbind_func = None
        self._unbind_args = tuple()

    def __call__(self, instance):
        return self.func(instance)

    def add_unbinder(self, func, *args):
        self._unbind_func = func
        self._unbind_args = args

    def unbind(self):
        func = self._unbind_func
        args = self._unbind_args
        self._unbind_func = None
        self._unbind_args = tuple()
        return func(*args)

