from ptutils.core.module import Module


class Coordinator(Module):

    def __init__(self, *args, **kwargs):
        super(Coordinator, self).__init__(*args, **kwargs)

        # Core
        self.estimator = None
        self.datastore = None
        self.dataprovider = None

        self.test_step = None
        self.train_step = None
        self.predict_step = None

        self.test_loop = None
        self.train_loop = None
        self.predict_loop = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        self._step_count = 0
        self._epoch_count = 0
        self._batch_count = 0


    def step(self):
        pass

    def loop(self):
        pass

    def run(self):
        pass


class Trainer(Coordinator):

    def train_step(self, input, target):

        self.estimator.optimizer.zero_grad()
        output = self.estimator.model(data)
        loss = self.estimator.criterion(output, target)
        self.estimator.optimize(loss)

        self.module.optimizer.zero_grad()
        output = self.module.forward(input)
        loss = self.module.loss(output, target)
        self.module.optimize(loss)
        self.module.state.up

    def train_loop(self, dataloader):
        for input in dataloader:
            self.train_step(data)

    def train(self):
        dataloader = self.dataprovider.provide()
        self.train_loop(dataloader)
