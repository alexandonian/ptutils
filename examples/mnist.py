import torch.nn as nn
import torch.optim as optim

from ptutils.nn.model import MNIST
from ptutils.core.trainer import Trainer
from ptutils.core.estimator import Estimator
from ptutils.dataprovider.data import MNISTProvider


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
        self.provider = MNISTProvider()
        self.estimator = MNISTEstimator()


trainer = MNISTTrainer()

trainer.run()
