from .entities import BaseEntity, ComponentDict
from .processes import BaseProcess


def _empty():
    pass


def _empty_arg(arg):
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

    def register_process(self, process, domain=None, priority=0, enter=_empty_arg,
                         exit=_empty_arg, startup=_empty, setup=_empty,
                         teardown=_empty, shutdown=_empty):
        if not domain:
            domain = set()
        for c in domain:
            if c not in self:
                self[c] = ComponentDict()
        domain_views = [self[k].keys() for k in domain]
        self._processes[process] = {"domain":domain, "enter":enter,
                                    "exit":exit, "startup":startup,
                                    "setup":setup, "teardown":teardown,
                                    "shutdown":shutdown, "priority":priority,
                                    "eids": set(), "domain_views": domain_views}
        self._process_queue.append(process)
        self._process_queue.sort(key=lambda x: self._processes[x]["priority"])

    def __call__(self):
        if self.running is False:
            for process in self._process_queue:
                self._processes[process]["startup"]()
            self.running = True
        for process in self._process_queue:
            process_data = self._processes[process]
            process_data["setup"]()
            domain_views = process_data["domain_views"]
            if domain_views:
                eids = list(set.intersection(*[set(s) for s in domain_views]))
            else:
                eids = list()
            previous_eids = process_data["eids"]
            entering = set(eids).difference(previous_eids)
            for eid in entering:
                process_data["enter"](self.Entity(eid))
                if self.is_in_domain(eid, process_data["domain"]):
                    process_data["eids"].add(eid)
                else:
                    eids.remove(eid)
            for eid in eids:
                process(self.Entity(eid))
            exiting = process_data["eids"].difference(eids)
            for eid in exiting:
                process_data["exit"](self.Entity(eid))
                if not self.is_in_domain(eid, process_data["domain"]):
                    process_data["eids"].remove(eid)
            process_data["teardown"]()

    def is_in_domain(self, eid, domain):
        for d in domain:
            if eid not in self[d]:
                return False
        return True

    def quit(self):
        self.running = False
        for process in self._process_queue:
            self._processes[process]["shutdown"]()

