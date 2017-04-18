import collections

namedtuple = collections.namedtuple


class ProcessManager:
    Process = namedtuple("Process", ["func", "domain", "domain_view", "setup", "teardown", "priority"])

    def __init__(self, components, entity_getter):
        self._queue = list()
        self._components = components
        self._entity_getter = entity_getter

    def register(self, func, domain=None, setup=None, teardown=None, priority=0):
        if domain:
            domain_view = self._components[domain].keys()
        else:
            domain_view = list()
        process = self.Process(func, domain, domain_view, setup, teardown, priority)
        self._queue.append(process)
        self._queue.sort(key=lambda p: p.priority)

    def __call__(self):
        for process in self._queue:
            if process.setup:
                process.setup()
            for eid in list(process.domain_view):
                process.func(self._entity_getter(eid))
            if process.teardown:
                process.teardown()
