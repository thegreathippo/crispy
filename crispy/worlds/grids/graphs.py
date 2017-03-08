class Graph(dict):
    def __init__(self, cells):
        super().__init__()
        for cell in cells:
            for cardinal in cell.cardinals:
                if cardinal in cells:
                    self.connect(cell, cardinal)
            for ordinal in cell.ordinals:
                if ordinal in cells:
                    u = ordinal[0], cell[1]
                    v = cell[0], ordinal[1]
                    if u in cells and v in cells:
                        self.connect(cell, ordinal)

    def add_node(self, u):
        if u not in self:
            self[u] = dict()

    def connect(self, u, v):
        if u not in self:
            self.add_node(u)
        if v not in self:
            self.add_node(v)
        if v not in self[u]:
            self[u][v] = dict()
            self[v][u] = dict()