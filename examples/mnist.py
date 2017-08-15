import torch.nn as nn
import torch.optim as optim

from ptutils.model import Model
from ptutils.net.layers.layers import MNIST
from ptutils.contrib.datasource import mnist
from ptutils.datastore import MongoDatastore
from ptutils.model.optimizer import Optimizer
from ptutils.coordinator.trainer import Trainer


class MNISTModel(Model):

    def __init__(self):
        super(MNISTModel, self).__init__()
        self.net = MNIST()
        self.learning_rate = 1e-3
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.net.parameters(), self.learning_rate)


class MNISTTrainer(Trainer):

    def __init__(self):
        super(MNISTTrainer, self).__init__()
        self.model = MNISTModel()
        self.datastore = MongoDatastore('testdb', 'testcol')
        self.datasource = mnist.MNISTSource()

    def step(self, input, target):
        super(MNISTTrainer, self).step(input, target)
        self.datastore.save({'step': self.global_step,
                             'loss': self.model._loss.data[0]})
        print(trainer.to_params())


trainer = MNISTTrainer()
# trainer.run()
# o = Optimizer('Adam')