"""Coordinator.

Coordinates and records interactions between objects.
"""
from ptutils.base.module import Module


class Coordinator(object):

    def __init__(self, *args, **kwargs):
        # super(Coordinator, self).__init__(*args, **kwargs)

        # Core
        self.provider = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        self._step_count = 0
        self._epoch_count = 0
        self._batch_count = 0

    def step(self):
        pass

    def loop(self):
        pass

    def run(self):
        pass
