"""Trainer.

A coordinator that trains one or several Models.

"""

from ptutils.model import Model
from coordinator import Coordinator


class Trainer(Coordinator):

    def __init__(self, model=None, datastore=None, datasource=None, **kwargs):
        super(Trainer, self).__init__(model=None,
                                      datastore=None,
                                      datasource=None,
                                      **kwargs)

        # Core
        # self._model = None
        # self._datastore = None
        # self._datasource = None

        self.test_step = None
        self.train_step = None
        self.predict_step = None

        self.test_loop = None
        self.train_loop = None
        self.predict_loop = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        # self._global_step = 0
        self._epoch_count = 0
        self._batch_count = 0

    def step(self, input, target):
        super(Trainer, self).step()

        self.model.forward(input, target)
        print('step: {}; loss: {}'.format(self.global_step,
                                          self.model._loss.data[0]))

    def loop(self, dataloader):
        for input, target in dataloader:
            self.step(input, target)

    def run(self):
        input = self.datasource.provide()
        self.loop(input)

    @property
    def model(self):
        return self._bases['model']

    @model.setter
    def model(self, value):
        self._bases['model'] = value

    @property
    def datasource(self):
        return self._bases['datasource']

    @datasource.setter
    def datasource(self, value):
        self._bases['datasource'] = value
