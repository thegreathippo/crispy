class GameObject:
    @property
    def x(self):
        try:
            return self.cell.x
        except AttributeError:
            return self.pos.x

    @x.setter
    def x(self, value):
        try:
            self.cell = value, self.cell.y, self.cell.z
        except AttributeError:
            self.pos = value, self.pos.y, self.pos.z

    @property
    def y(self):
        try:
            return self.cell.y
        except AttributeError:
            return self.pos.y

    @y.setter
    def y(self, value):
        try:
            self.cell = self.cell.x, value, self.cell.z
        except AttributeError:
            self.pos = self.pos.x, value, self.pos.z

    @property
    def z(self):
        try:
            return self.cell.z
        except AttributeError:
            return self.pos.z

    @z.setter
    def z(self, value):
        try:
            self.cell = self.cell.x, self.cell.y, value
        except AttributeError:
            self.pos = self.pos.x, self.pos.y, value

