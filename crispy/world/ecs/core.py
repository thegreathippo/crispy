from ..ecs.entities import Root


class System(Root):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._processes = dict()
        self._queue = list()

    def register_process(self, process, domain, priority=0):
        if domain not in self:
            self[domain] = dict()
        domain_view = self[domain].keys()
        self._processes[process] = {"domain": domain_view, "priority": priority}
        self._queue.append(process)
        self._queue.sort(key=lambda x: self._processes[x]["priority"])

    def __call__(self):
        for process in self._queue:
            domain = self._processes[process]["domain"]
            for eid in domain:
                process(self.get_entity(eid))

