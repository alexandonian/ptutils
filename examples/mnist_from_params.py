import torch.nn as nn
import torch.optim as optim

from ptutils.net.model import MNIST
from ptutils.net.optimizer import Optimizer
from ptutils.contrib.datasource import mnist
from ptutils.model.estimator import Estimator
from ptutils.coordinator.trainer import Trainer
from ptutils.base.configuration import Configuration


params = {
    'lr': 1e-3,
    'model': {MNIST: {}},
    'criterion': {nn.CrossEntropyLoss: {}},
    'optimizer': {Optimizer: {
        'optimizer': 'Adam'
    }}
}

config = Configuration(params)

class MNISTEstimator(Estimator):

    def __init__(self):
        super(MNISTEstimator, self).__init__()
        self._lr = 1e-3
        self._model = MNIST()
        self._criterion = nn.CrossEntropyLoss()
        self._optimizer = optim.Adam(self._model.parameters(), self._lr)


class MNISTTrainer(Trainer):

    def __init__(self):
        super(MNISTTrainer, self).__init__()
        self.estimator = MNISTEstimator()
        self.provider = mnist.MNISTProvider()


# trainer = MNISTTrainer()
# trainer.run()
