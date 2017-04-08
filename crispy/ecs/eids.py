class EIDRef:
    def __init__(self):
        self.refs = {0: 0}
        self.free = set()
        self._high = 0

    def increment(self, eid):
        if eid not in self.refs:
            self.refs[eid] = 0
            self.free.discard(eid)
            if eid > self._high:
                self._high = eid
        self.refs[eid] += 1

    def decrement(self, eid):
        self.refs[eid] -= 1
        if self.refs[eid] == 0 and eid != 0:
            del self.refs[eid]
            self.free.add(eid)

    def get_next(self):
        if self.free:
            return self.free.pop()
        else:
            return self._high + 1

    def clear(self):
        self.refs = {0: 0}
        self.free = set()
        self._high = 0



