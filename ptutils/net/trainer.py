

class Trainer(object):
    def __init__(self, model=None, **kwargs):
        super(Trainer, self).__init__(**kwargs)

        # Core
        self._model = None
        self._criterion = None
        self._optimizer = None

        self._loop = Loop()  # .bind_module(self)
        self._function = Function().register_module(self)
        self._callbacks = callback.CallbackEngine().bind_module(self)

        self._meta = TrainMeta()
        # self.spec = State()
        # self.state = State()
        # self.config = State()
        # self.history = History()

    def train_function(self, input, target):
        self._callbacks.call(self._callbacks.PRE_TRAINING_STEP)
        self._function.train(input, target)
        self._callbacks.call(self._callbacks.POST_TRAINING_STEP)
        if self._has_metrics:
            self._state.update({name: metric(output, target)
                                for name, metric in self.metrics.items()})
        self.history.append(self._state)

    def train_epoch(self):
        self._callbacks.call(self._callbacks.PRE_EPOCH)
        for i, (input, target) in enumerate(dataloader):
            target = target.cuda(async=True)
            input_var = Variable(input, volatile=volatile).cuda()
            target_var = Variable(target, volatile=volatile).cuda()
            self.train_function(input_var, target_var)

            if self.validate_now:
                pass
            if self.save_now:
                pass
        self._callbacks.call(self._callbacks.POST_EPOCH)

    def train(self):
        self._callbacks.call(self._callbacks.PRE_TRAINING)

        for epoch in range(self.config.get('epochs')):
            self.train_epoch()

        self._callbacks.call(self._callbacks.POST_TRAINING)


class TrainConfig(meta.Config):
    def __init__(self):
        self.data_config = None
        self.queue_config = None
        self.num_steps = 500


class TrainSpec(meta.Spec):
    pass


class TrainStats(meta.Stats):
    pass


class TrainState(meta.State):
    def __init__(self):
        self.step = 0
        self.epoch = 0
        self.batch = 0
        self.stats = None


class TrainHistory(meta.History):
    def __init__(self):
        self.states = []
        self.global_stats = Stats()
        self.best_stats = Stats()

    def record(self, state):
        self.states.append((state.step, state))
        for name, stat in state.stats.items():
            if stat > self.best_stats[name]:
                self.best_stats[name] = stat


class TrainMeta(meta.Meta):
    def __init__(self):
        self.spec = TrainSpec()
        self.state = TrainState()
        self.config = TrainConfig()
        self.history = TrainHistory()
        self.callbacks = Callbacks()

    def update_batch(self, stats=None):
        self.state.stats = stats
        self.history.record(self.state)
        self.state.step += 1
        self.state.batch += 1

    def update_step(self, state):
        self.state.step += 1
        self.history.record(state)

    def update_epoch(self, state):
        self.state.step += 1
        self.state.epoch += 1
        self.history.record(state)
