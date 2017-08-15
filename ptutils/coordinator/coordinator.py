"""Coordinator.

Coordinates and records interactions between ptutils objects.
"""
from ptutils.base.module import NullModule as Module


class Coordinator(Module):

    def __init__(self, *args, **kwargs):
        # super(Coordinator, self).__init__(*args, **kwargs)

        # Core
        self._datastore = None

        # Iteration and epoch book-keeping
        # Replace with Coordinator_ state mod
        self._step = 0

    def step(self):
        pass

    def loop(self):
        pass

    def run(self):
        pass

    @property
    def datastore(self):
        return self._datastore