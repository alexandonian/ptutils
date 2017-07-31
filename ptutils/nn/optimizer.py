import torch.optim as optim


class Optimizer(optim.Optimizer, base.Optimizer):
    __name__ = 'optimizer'

    def __init__(self, optimizer):
        base.Optimizer.__init__(self)
        self.state = defaultdict(dict)
        self.param_groups = []
        self.optimizer_cls = optimizer

    def step(self, closure=None):
        return self.optimizer(closure=closure)

    def zero_grads(self):
        return self.optimizer.zero_grads()
