import torch.nn as nn
import torch.optim as optim

from ptutils.model import Model
from ptutils.net.model import MNIST
from ptutils.contrib.datasource import mnist
from ptutils.coordinator.trainer import Trainer


class MNISTModel(MNIST):

    def __init__(self):
        super(MNIST, self).__init__()
        self._lr = 1e-3
        self._criterion = nn.CrossEntropyLoss()
        self._optimizer = optim.Adam(self.parameters(), self._lr)


class MNISTTrainer(Trainer):

    def __init__(self):
        super(MNISTTrainer, self).__init__()
        # self.model = MNIST()
        self.provider = mnist.MNISTProvider()


trainer = MNISTTrainer()
trainer.run()
