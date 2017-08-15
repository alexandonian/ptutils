"""Trainer.

A coordinator that trains one or several Models.

"""

from ptutils.model import Model
from coordinator import Coordinator


class Trainer(Coordinator):

    def __init__(self, model=None, datastore=None, datasource=None, **kwargs):
        super(Trainer, self).__init__(self,
                                      model=None,
                                      datastore=None,
                                      datasource=None)

        # Core
        self._model = None
        self._datastore = None
        self._datasource= None

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

        self.model(input, target)
        self._step_count += 1
        print('step: {}; loss: {}'.format(self._step_count,
                                          self.estimator._loss.data[0]))

    def loop(self, dataloader):
        for input, target in dataloader:
            self.step(input, target)

    def run(self):
        input = self.provider.provide()
        self.loop(dataloader)

    @property
    def model(self):
        return self._model

    @property
    def datasource(self):
        return self._datasource