class WorldObject:
    @property
    def x(self):
        try:
            return self.cell[0]
        except AttributeError:
            return self.pos[0]

    @x.setter
    def x(self, value):
        try:
            self.cell = value, self.cell[1], self.cell[2]
        except AttributeError:
            self.pos = value, self.pos[1], self.pos[2]

    @property
    def y(self):
        try:
            return self.cell[1]
        except AttributeError:
            return self.pos[1]

    @y.setter
    def y(self, value):
        try:
            self.cell = self.cell[0], value, self.cell[2]
        except AttributeError:
            self.pos = self.pos[0], value, self.pos[2]

    @property
    def z(self):
        try:
            return self.cell[2]
        except AttributeError:
            return self.pos[2]

    @z.setter
    def z(self, value):
        try:
            self.cell = self.cell[0], self.cell[1], value
        except AttributeError:
            self.pos = self.pos[0], self.pos[1], value

