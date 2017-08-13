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


class Optimizer(torch.optim.Optimizer):
    def __init__(self, optimizer, param_groups=None, **kwargs):
        """
        Builds the optimizer for training.

        Parameters
        ----------
        optimizer : str or callable
            Name of the optimizer when str, handle to the optimizer class when callable.
            If a name is provided, this optimizer looks for the optimizer in `torch.optim`
            module first and in inferno.extensions.optimizers second.
        param_groups : list of dict
            Specifies the parameter group. Defaults to model.parameters() if None.
        kwargs : dict
            Keyword arguments to the optimizer.

        Returns
        -------
        Trainer
            self.

        Raises
        ------
        AssertionError
            if optimizer is not found
        NotImplementedError
            if optimizer is not str or callable.
        """
        if isinstance(optimizer, str):
            optimizer_class = getattr(torch.optim, optimizer, None)
            if optimizer_class is None:
                # Look for optimizer in extensions
                optimizer_class = getattr(optimizers, optimizer, None)
            assert optimizer_class is not None, "Optimizer {} not found.".format(
                optimizer)
        elif callable(optimizer):
            optimizer_class = optimizer
        else:
            raise NotImplementedError
        param_groups = self.model.parameters() if param_groups is None else param_groups
        self._optimizer = optimizer_class(param_groups, **kwargs)

    def compute_gradients(self, loss):
        loss.backward()

    def apply_gradients(self):
        self.step()

    def optimize(self, loss):
        self.compute_gradients(loss)
        self.apply_gradients()
