"""Estimator.

Encapsulates a neural network model, criterion and optimizer.
"""
import torch
from torch.autograd import Variable
from torch.nn.parallel import data_parallel

from ptutils.base.module import Module


class Estimator(Module):

    def __init__(self, *args, **kwargs):
        super(Estimator, self).__init__(*args, **kwargs)

        # Core
        self._model = None
        self._criterion = None
        self._optimizer = None

        # GPU and dtype business
        # Replace with estimator_spec mod
        self._dtype = 'float'
        self._devices = None
        self._use_cuda = torch.cuda.is_available()
        # self._use_cuda = False

        # self.model = torch.nn.DataParallel(self.model).cuda()

        # use_cuda = torch.cuda.is_available()
        # dtype = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor

        # if use_cuda:
        #     self.model.cuda()
        #     self.criterion.cuda()

        # # Select mode
        # if mode == 'train':
        #     self.model.train()
        #     volatile = False
        # else:
        #     self.model.eval()
        #     volatile = True

        self._loss = None

    def forward(self, input):
        input_var = Variable(input)
        if self._devices is not None:
            return data_parallel(self.model, input_var, list(self._devices))
        else:
            return self.model(input_var)

    def loss(self, output, target):
        target_var = Variable(target)
        loss = self._criterion(output, target_var)
        return loss

    def compute_gradients(self, loss=None):
        loss = self._state.get('loss') if loss is None else loss
        # if self.optimizer is not None:
            # self.optimizer.compute_gradients(loss)
        # else:
            # loss.backward()
        loss.backward()

    def apply_gradients(self):
        # self.optimizer.apply_gradients()
        self.optimizer.step()

    def optimize(self, loss=None):
        self.compute_gradients(loss=loss)
        self.apply_gradients()
        self.optimizer.zero_grad()

    def step(self, input, target):
        output = self.forward(input)
        self._loss = self.loss(output, target)
        self.optimize(self._loss)

    @property
    def model(self):
        return self._model

    @property
    def criterion(self):
        return self._criterion

    @property
    def optimizer(self):
        return self._optimizer
