"""Contains the ProcessManager class; which inherits from ComponentManager.

Instances of the ProcessManager class provide component handling via its
base (ComponentManager), while assuming responsibility for registering and
running processes.
"""
from .components import ComponentManager
from .utils import required_num_of_args
from collections import namedtuple


class ProcessManager(ComponentManager):
    Process = namedtuple("Process", ["func", "domain", "domain_view", "setup", "teardown", "priority"])

    def __init__(self):
        """Initialize the ProcessManager class instance.

        ATTRIBUTES:
          _queue (list): A list of processes maintained in order
            of their priority.
        """
        super().__init__()
        self._queue = list()

    def register_process(self, process, domain, setup=None, teardown=None, priority=0):
        """Register a process.

          ARGUMENTS:
            process: A callable object that accepts at least one
              argument (the entity).
            domain (str): The component associated with this process.
              Every 'step', all entities with this component will
              be passed to the process.
            setup (callable): A function to be called when this process
              is being set up. Defaults to None.
            teardown (callable): A function to be called when this
              process is being torn down. Defaults to None.
            priority (int): The order of this process in relation to
              other processes. Processes with a higher priority will
              be handled first. Defaults to 0.

          EXCEPTIONS:
            TypeError: Raised if the process is either not callable or
              does not accept the correct number of arguments (1).
            KeyError: Raised if the domain (component) is not actually
              in this instance.
        """
        num = required_num_of_args(process)
        if num != 1:
            raise TypeError("{0} must need 1 arg; needs {1}".format(process, num))
        domain_view = self[domain].keys()
        proc = self.Process(process, domain, domain_view, setup, teardown, priority)
        self._queue.append(proc)
        self._queue.sort(key=lambda x: x.priority, reverse=True)

    def __call__(self):
        for process in self._queue:
            if process.setup:
                process.setup()
            for eid in process.domain_view:
                process.func(self.Entity(eid))
            if process.teardown:
                process.teardown()
