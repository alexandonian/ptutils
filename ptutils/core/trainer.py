"""Trainer.

A coordinator that trains estimators.
"""

from estimator import Estimator
from coordinator import Coordinator


class Trainer(Coordinator):

    def __init__(self, datastore=None, estimator=None, provider=None, **kwargs):
        super(Trainer, self).__init__(self,
                                      datastore=None,
                                      estimator=None,
                                      provider=None,
                                      **kwargs)

        # Core
        self._provider = None
        self._estimator = None
        self._datastore = None

        self.test_step = None
        self.train_step = None
        self.predict_step = None

        self.test_loop = None
        self.train_loop = None
        self.predict_loop = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        self._step_count = 0
        self._epoch_count = 0
        self._batch_count = 0

    def step(self, input, target):

        self.estimator.step(input, target)
        self._step_count += 1
        print('step: {}; loss: {}'.format(self._step_count,
                                          self.estimator._loss.data[0]))

    def loop(self, dataloader):
        for input, target in dataloader:
            self.step(input, target)

    def run(self):
        dataloader = self.provider.provide()
        self.loop(dataloader)
