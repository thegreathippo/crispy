from . import actions


def move(entity, direction):
    x, y, z = entity.cell
    vx, vy, vz = direction
    pos = x + vx, y + vy, z + vz
    entity.cell = pos
    entity.sprite = pos[0], pos[1], pos[2], entity.sprite[3]


@actions.abstract
class Move(actions.Action):
    subjects = ["agent"]
    direction = (0, 0, 0)


@actions.abstract
class Step(Move):
    subjects = ["agent"]
    direction = (0, 0, 0)
    cost = 5

    def before(self):
        self.direction = self.direction

    def after(self):
        try:
            move(self.subjects[0], self.direction)
        except ValueError as e:
            self.cost = 0
            raise e


class NoStep(Step):
    direction = (0, 0, 0)


class StepNorth(Step):
    direction = (0, 1, 0)


class StepSouth(Step):
    direction = (0, -1, 0)


class StepEast(Step):
    direction = (1, 0, 0)


class StepWest(Step):
    direction = (-1, 0, 0)


class StepNorthEast(Step):
    direction = (1, 1, 0)


class StepNorthWest(Step):
    direction = (-1, 1, 0)


class StepSouthWest(Step):
    direction = (-1, -1, 0)


class StepSouthEast(Step):
    direction = (1, -1, 0)


_steps = [NoStep, StepNorth, StepWest, StepSouth, StepEast, StepNorthWest, StepNorthEast, StepSouthWest,
          StepSouthEast]
steps = dict()
for s in _steps:
    steps[s.direction] = s
