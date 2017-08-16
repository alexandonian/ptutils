import torch.nn as nn
import torch.optim as optim


from ptutils.model import Model
from ptutils.model.net import MNIST
from ptutils.contrib.datasource import mnist
from ptutils.datastore import MongoDatastore
from ptutils.model.optimizer import Optimizer
from ptutils.coordinator.trainer import Trainer

# params = {
# 'lr': 1e-3,
# 'model': {MNIST: {}},
# 'criterion': {nn.CrossEntropyLoss: {}},
# 'optimizer': {Optimizer: {
#     'optimizer': 'Adam'
# }}
# }


params = {
    'name': 'mnist_trainer',
    'exp_id': 'my_experiment',
    'my_model': {
        Model: {
            'name': 'MNISTModel',
            'net': 'net'}},
    'my_datastore': {MongoDatastore: {}},
    'my_datasource': {mnist.MNISTSource: {}}}


trainer = Trainer.from_params(params)
# print(trainer)
# print(trainer.to_params())


# trainer = MNISTTrainer()
# trainer.run()
