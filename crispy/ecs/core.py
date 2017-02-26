from .entities import BaseEntity
from .processes import BaseProcess
import kivy


def _empty():
    pass


class System(dict):

    def __init__(self):
        super().__init__()
        self._processes = dict()
        self._process_queue = list()
        self.eid = 0
        self.running = False

        class Entity(BaseEntity):
            root = self

        class Process(BaseProcess):
            root = self

        self.Entity = Entity
        self.Process = Process

    def register_process(self, process, domain=None, priority=0, startup=_empty,
                         setup=_empty, teardown=_empty, shutdown=_empty):
        if not domain:
            domain = set()

        # add exception here for invalid domains? IE, domains with components that
        # don't exist?
        domain_dict = {k: v for k, v in self.items() if k in domain}
        self._processes[process] = {"domain": domain_dict, "startup": startup,
                                    "setup": setup, "teardown": teardown,
                                    "shutdown": shutdown, "priority": priority}
        self._process_queue.append(process)
        self._process_queue.sort(key=lambda x: self._processes[x]["priority"])

    def step(self):
        if self.running is False:
            for process in self._process_queue:
                self._processes[process]["startup"]()
            self.running = True
        for process in self._process_queue:
            self._processes[process]["setup"]()
            domain = self._processes[process]["domain"]
            if domain:
                eids = list(set.intersection(*[set(s) for s in domain.values()]))
            else:
                eids = list()
            for eid in eids:
                process(self.Entity(eid))
            self._processes[process]["teardown"]()

    def quit(self):
        self.running = False
        for process in self._process_queue:
            self._processes[process]["shutdown"]()
