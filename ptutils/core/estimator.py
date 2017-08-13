from torch.nn.parallel import DataParallel
from ptutils.core.module import Module


class Estimator(Module):

    def __init__(self, *args, **kwargs):

        # Core
        self._model = None
        self._criterion = None
        self._optimizer = None

        # GPU and dtype business
        # Replace with estimator_spec mod
        self._dtype = 'float'
        self._devices = None
        self._use_cuda = False

    def forward(self, *input):
        if self._devices is not None:
            return DataParallel(self.model, input, list(self._devices))
        else:
            return self.model(*input)

    def loss(self, output, target):
        loss = self._criterion(output, target)
        return loss

    def compute_gradients(self, loss=None):
        loss = self._state.get('loss') if loss is None else loss
        if self.optimizer is not None:
            self.optimizer.compute_gradients(loss)
        else:
            loss.backward()

    def apply_gradients(self):
        self.optimizer.apply_gradients()

    def optimize(self, loss=None):
        self.compute_gradients(loss=loss)
        self.apply_gradients()
        self.optimizer.zero_grad()

    def fit(self, input, target):
        output = self.forward(input)
        loss = self.loss(output, target)
        self.optimize(loss)

    @property
    def model(self):
        return self._model

    @property
    def criterion(self):
        return self._criterion

    @property
    def optimizer(self):
        return self._optimizer
