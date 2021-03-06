from . import core


class Move(core.Action):
    direction = (0, 0, 0)


class Step(Move):
    direction = (0, 0, 0)
    cost = 5


class NoStep(Step):
    direction = (0, 0, 0)
    cost = 1


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
