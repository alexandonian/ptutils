"""Coordinator.

Coordinates and records interactions between ptutils objects.

"""
from ptutils.base import Base
from ptutils.utils.exceptions import StepError


class Coordinator(Base):

    def __init__(self, *args, **kwargs):
        super(Coordinator, self).__init__(*args, **kwargs)

        # Core
        self._exp_id = None
        self._global_step = 0
        # self._datastore = None

    def step(self):
        self.global_step += 1

    def loop(self):
        pass

    def run(self):
        pass

    @property
    def datastore(self):
        return self._bases['datastore']

    @datastore.setter
    def datastore(self, value):
        self._bases['datastore'] = value

    @property
    def exp_id(self):
        return self._exp_id

    @exp_id.setter
    def exp_id(self, value):
        self._exp_id = value

    @property
    def global_step(self):
        return self._global_step

    @global_step.setter
    def global_step(self, value):
        if value <= self._global_step:
            raise StepError('The global step should have been incremented.')
        elif value > (self._global_step + 1):
            raise StepError('The global step can only be incremented by one.')
        else:
            self._global_step = value
