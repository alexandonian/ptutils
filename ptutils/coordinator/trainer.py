"""Trainer.

A coordinator that trains one or several Models.

"""

from ptutils.model import Model
from coordinator import Coordinator


class Runner(Base):

    def __init__(self, model=None, datastore=None, datasource=None, **kwargs):
        super(Trainer, self).__init__(model=None,
                                      datastore=None,
                                      datasource=None,
                                      **kwargs)

        # Core
        # self._model = None
        # self._datastore = None
        # self._datasource = None

        # self.test_step = None
        # self.train_step = None
        # self.predict_step = None

        # self.test_loop = None
        # self.train_loop = None
        # self.predict_loop = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        # self._global_step = 0
        # self._epoch_count = 0
        # self._batch_count = 0

    #tfutils train_loop
    def step(self, input, target):
        """Defines a single step of an experiment.

        This must increment the global step. A common use case
        will be to simply make a forward pass update the model.

        Formally, this will call model.forward(), whose output should
        be used by the dataprovider to provide the next batch of data.

        """
        super(Trainer, self).step()

        output = self.model.forward(input, target)
        print('step: {}; loss: {}'.format(self.global_step,
                                          self.model._loss.data[0]))

    #tfutils train
    def loop(self, dataloader):
        """Defines the primary training loop.

        The default is to just step the trainer.

        """
        # Step the Trainer
        for input, target in dataloader:
            self.step(input, target)

            # You may want to do additional computation
            # in between steps.
    # train_from_params
    def run(self):
        """Runs the execution of an experiment.

        This is the primary entrance to the Trainer class.

        """
        # Do any initialization needed here
        input = self.datasource.provide()

        # Start the main training loop.
        self.loop(input)

        # Perhaps you do validation at this point

        # Do any cleanup needed to conclude the experiment.

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
