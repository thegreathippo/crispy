class _ProcessType(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if cls.root:
            process = cls()
            cls.root.register_process(process.run, priority=process.priority,
                                      domain=process.domain,
                                      startup=process.startup,
                                      setup=process.setup,
                                      teardown=process.teardown,
                                      shutdown=process.shutdown)
        return cls


class BaseProcess(metaclass=_ProcessType):
    priority = 0
    domain = set()
    root = None

    def startup(self):
        pass

    def setup(self):
        pass

    def enter(self, entity):
        pass

    def run(self, entity):
        pass

    def exit(self, entity):
        pass

    def teardown(self):
        pass

    def shutdown(self):
        pass
