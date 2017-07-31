""""ptutils base module.

This module contains the ptutils base class definitions:

    - `Module`
    - `State`
    - `Status`
    - `Configuration`

At the core of PTUtils is the `Module`class, the base class for all ptutils
classes that attempts to generalize PyTorch's existing `torch.nn.Module`.
A `Module` is an arbitrary, container-like class that fulfills three simple
requirements:

1. A `Module` must be callable. A `Module` may maintain any desired number
of public and private methods, although it must separately implement the
`__call__` method, which may simply map to one of its other methods.

2. A `Module` must implement a `state()` method that returns an instance of
a `State` module. This state module should reflect the current 'state' of the
module and can be explicity specified by the user.

3. A `Module` must implement a `load_state()` method that restores the module
to the state described by a given state module.

A `State` module (henceforth ref) serves as a specialized 'identity' module that preserves
the following:

```python
    s = s(*args, **kwargs)
      = s.state(*args, **kwargs)
      = s.load_state(*args, **kwargs),
```
where `s` is an instance of the `State` class.

Critically, a module can register and operate other modules as regular
attributes, allowing users to nest them in a tree structure. All other,
non-module attributes are considered to be 'properties' of that module.
By default, the state module returned by a module's `state` method contains
the properties of that module and the state module

Enforcing this simple API attempts to address the notion that the environment
in which a neural network operates should be free to evolve dynamically just
as the network itself is.


"""

import torch
import torch.nn as nn

import ptutils.core.module as module


###############################################################################
# MODULE
###############################################################################

class Module(module.Module):

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        super(Module, self).__setattr__(name, value)
        if isinstance(value, Module):
            pass
            # self.add_module(name, value)
            # base = value.__base__
            # object.__setattr__(self, '_' + base.lower(), value)


class MetaModule(Module):
    pass

###############################################################################
# CORE: Module Containers
###############################################################################


class ModuleList(Module):
    pass


class Step(Module):
    pass


class GlobalStep(Step):
    pass


class Epoch(Module):
    pass


class Checkpoint(Module):

    def __init__(self,
                 id=None,
                 sess_id=None,
                 config=None,
                 step=None,
                 epoch=None,
                 module=None,
                 state_dict=None,
                 optimizer=None,
                 **kwargs):
        self.step = step
        self.epoch = epoch
        self.module = module
        self.state_dict = state_dict
        self.optimizer = optimizer


class Cache(Module):
    pass


class State(module.State):
    pass


class TrainState(State):

    def __init__(self, name):

        self.name = name  # This ends up being the _id
        self.config = config

        # Epoch Variables
        self.global_epoch = 1
        self.epoch_losses = []
        self.epoch_accs = []
        self.epoch_times = []
        self.cum_epoch_loss = 0.
        self.cum_epoch_acc = 0.
        self.best_epoch_acc = 0.

        # Step Variables
        self.global_step = 1
        self.epoch_step_times = []  # only keep for one epoch
        self.cum_loss = 0.
        self.cum_acc = 0.

        # Tuning Variables
        self.tuning_accs = []


class History(State):

    def __init__(self):
        self.trainstates = []
        self.checkpoints = []

    # something like this
    def add_state(self, trainstate):
        self.trainstates.append(trainstate)

    def add_checkpoint(self, checkpoint):
        self.checkpoints.append(checkpoint)

    def update(self, trainstate, checkpoint):
        self.add_state(trainstate)
        self.add_checkpoint(checkpoint)


class Status(MetaModule):

    @classmethod
    def verify(cls):
        pass


class Batch(Module):
    pass


class HyperParams(Module):
    pass


class Signal(Module):
    pass


class Specification(MetaModule):
    pass


class DeviceSpec(Specification):
    pass


class ClusterSpec(Specification):
    pass


class Registry(Module):
    pass


class Benchmark(Module):
    pass


class Plugin(Module):
    pass


class Device(MetaModule):
    @classmethod
    def manage(cls):
        pass


class Cluster(MetaModule):
    pass


class Backend(Module):
    pass


class Configuration(MetaModule):
    _io = IO()
    _parser = Parser()
    _datahandler = DataHandler()

    def __init__(self, config=None):
        super(Configuration, self).__init__()
        config = self._datahandler.load(config)
        parsed_config = _parser(config)
        self.config = parsed_config

    @classmethod
    def configure(cls, config):
        print(config)

    def __call__(self, config=None):
        if config is not None:
            return self.configure(config)
        else:
            return self.configure(self.config)


class DataSource(Module):
    pass


###############################################################################
# CORE: Operators: modules that performer specific tasks.
###############################################################################

class Scoper(Module):
    pass


class Handler(Module):
    pass


class Coordinator(Module):
    pass


class Supervisor(Module):
    pass


class Manager(Module):
    pass


class Scheduler(Module):
    pass


class LearningRateScheduler(Scheduler):
    def exponential_decay(self):
        pass

    def piecewise_constant(self):
        pass

    def polynomial_decay(self):
        pass

    def natural_exp_decay(self):
        pass

    def inverse_time_decay(self):
        pass


class Debugger(Module):
    pass


class Creator(Module):
    pass


class Converter(Module):
    pass


class Parser(Module):
    pass


class Saver(Module):

    _datasource = DataSource()
    _serializer = Serializer()

    @classmethod
    def save(cls):
        pass


class Loader(Module):

    _datasource = DataSource()
    _serializer = Serializer()

    @classmethod
    def load(cls):
        pass


class Reader(Module):

    @classmethod
    def read(cls):
        pass


class Writer(Module):

    @classmethod
    def write(cls):
        pass


class IO(Module):
    _Reader = Reader()
    _Writer = Writer()
    pass


class Serializer(Module):
    _encoder = Encoder()
    _decoder = Decoder()
    pass


class Formatter(Module):
    pass


class Encoder(Module):
    _backend = Backend()
    pass


class Decoder(Module):
    _backend = Backend()
    pass


class Logger(Module):
    _formatter = Formatter()


class Provider(Module):

    @classmethod
    def provider(cls):
        pass


class DataInterface(Module):
    _formatter = Formatter()
    _serializer = Serializer()
    pass


class Session(Module):
    _status = Status()
    _specification = Specification()
    _configuration = Configuration()
    _dataprovider = DataProvider()
    _database = Database()
    _estimator = Estimator()
    _step = Step()

    @classmethod
    def run(self):
        pass

    def __call__(self):
        return self.run()


class Optimizer(Module):

    def step(self):
        pass

    __call__ = step


class Criterion(Module):
    pass


class LearningRate(Module):
    pass


class Database(Module):

    @classmethod
    def access(cls):
        pass


class DBInterface(Module):
    pass


class DataProvider(Provider):

    @classmethod
    def provide(cls):
        pass


class Dataset(Module):
    _datastore = DataStore()
    pass


class Estimator(Module):

    allowed_kwargs = {'input_shape',
                      'batch_input_shape',
                      'batch_size',
                      'dtype',
                      'name',
                      'trainable',
                      'weights',
                      'input_dtype',  # legacy
                      }

    def __init__(self, model=None):

        if model is not None:
            if not isinstance(model, nn.Module):
                raise ValueError('model argument must inherit from torch.nn.Module')
            self.model = model

        # Core
        self._model = None
        self._criterion = None
        self._optimizer = None

        self.test_function = None
        self.train_function = None
        self.predict_function = None

        self.test_loop = None
        self.train_loop = None
        self.predict_loop = None

        # Iteration and epoch book-keeping
        # Replace with estimator_state mod
        self._iteration_count = 0
        self._epoch_count = 0
        self._batch_count = 0

        # GPU and dtype business
        # Replace with estimator_spec mod
        self._dtype = 'float'
        self._devices = None
        self._use_cuda = False

        # Validation
        self._save_at_best_validation_score = True
        self._best_validation_score = None
        self._is_iteration_with_best_validation_score = False
        self._validate_every = None
        self._num_validation_iterations = None
        # We should exclude the zero-th epoch from validation
        self._last_validated_at_epoch = 0
        # This is to allow a callback to trigger a validation by setting
        # trainer.validate_now = True
        self._validation_externally_triggered = False

        # History and Checkpointing
        self._save_every = None
        self._save_to_directory = None
        # Nothing to save at epoch 0
        self._last_saved_at_epoch = 0
        # This is to allow a callback to trigger a save by setting trainer.save_now = True
        self._save_externally_triggered = False

        # Stopping conditions
        self._max_num_iterations = None
        self._max_num_epochs = None

        # Callbacks and states
        self._callback_engine = CallbackEngine().bind_trainer(self)
        self._state = {}

        self._callbacks = []
        self._initializers = []
        self._regularizers = []

        # constraints
        self._metrics = []
        self._constraints = []
        self._has_constraints = False

        # metrics
        self._has_metrics = False

        # transforms
        self._transforms = []


    def initializer(self):
        pass

    def forward(self, *input):
        if self._devices is not None:
            return data_parallel(self.model, input, list(self._devices))
        else:
            return self.model(*input)

    def inference(self, *input):
        return self.forward(*input)

    def fprop(self, *input):
        return self.forward(*input)

    def loss(self, output, target):
        pass

    def config(self):
        pass

    def load(self):
        pass

    def evaluate(self):
        pass

    def compute_output(self, *input):
        return self._module(*input)

    def compute_loss(self, output):
        return self._criterion(output)

    def optimize(self):
        self._optimizer.step()

    def save(self):
        pass

    def fit(self):
        pass

    def feed_data(self):
        pass

    def step(self, batch):
        loss, acc = self.model.forward(batch)
        self.model.optimize(loss)

    def optimize(self):
        pass

    def evaluate(self):
        pass

    def train(self):
        while not self._stopping_condition_met():
            self._start_epoch()
            for _, batch in enumerate(self.train_batcher):
                self._start_step()
                loss, acc = self.step(batch)
                self._end_step(loss, acc)
            self._tuning()
            self._end_epoch()

    def _checkpoint(self, is_best):
        file_path = base.model_path(self.name, is_best)
        save_model(self.model, file_path)

    def _load_last(self):
        file_path = base.model_path(self.name, False)
        load_model(self.model, file_path)

    def _tuning(self):
        self.model.eval()
        cum_acc = 0.
        for _, batch in enumerate(self.tune_batcher):
            batch = self.tune_batcher.next_batch()
            _, acc = self.model.forward(batch)
            cum_acc += acc
        tuning_acc = cum_acc / len(self.tune_batcher)
        avg_acc, change_acc = self.history.end_tuning(tuning_acc)
        print('Average tuning accuracy: %5.3f%% (%s%5.3f%%)' %
              (avg_acc * 100,
               '+' if change_acc > 0 else '',
               change_acc * 100))
        self.model.train()


class Trainer(Module):
    _Model = Model()
    _DataProvider = DataProvider()

    def __init__(self):
        self._model = None
        self._criterion = None
        self._optimizer = None
        self._metric = None

    @classmethod
    def train(cls):
        pass


class Tester(Module):
    _Model = Model()
    _DataProvider = DataProvider()

    @classmethod
    def test(cls):
        pass


class Estimator(Module):
    _Trainer = Trainer()
    _Tester = Tester()

    def evaluate(self):
        pass

    def predict(self):
        pass

    def train(self):
        return self._trainer.train()

    def test(self):
        return self._tester.test()

    def predict_on_batch(self):
        pass

    def train_on_batch(self):
        pass

    def test_on_batch(self):
        pass


class Runner(Module):
    _Trainer = Trainer()
    _Tester = Tester()

    @classmethod
    def run(cls):
        pass


class Tuner(Module):
    pass


class Profiler(Module):
    pass


class Distributer(Module):
    pass


class Syncer(Module):
    pass


class Finder(Module):
    pass


class Inspector(Module):
    pass


class Importer(Module):
    pass


class Summarizer(Module):
    def summary(input_size, model):

        def register_hook(module):
            def hook(module, input, output):
                class_name = str(module.__class__).split('.')[-1].split("'")[0]
                module_idx = len(summary)

                m_key = '%s-%i' % (class_name, module_idx + 1)
                summary[m_key] = OrderedDict()
                summary[m_key]['input_shape'] = list(input[0].size())
                summary[m_key]['input_shape'][0] = -1
                summary[m_key]['output_shape'] = list(output.size())
                summary[m_key]['output_shape'][0] = -1

                params = 0
                if hasattr(module, 'weight'):
                    params += th.prod(th.LongTensor(list(module.weight.size())))
                    if module.weight.requires_grad:
                        summary[m_key]['trainable'] = True
                    else:
                        summary[m_key]['trainable'] = False
                if hasattr(module, 'bias'):
                    params += th.prod(th.LongTensor(list(module.bias.size())))
                summary[m_key]['nb_params'] = params

            if not isinstance(module, nn.Sequential) and \
               not isinstance(module, nn.ModuleList) and \
               not (module == model):
                hooks.append(module.register_forward_hook(hook))

        # check if there are multiple inputs to the network
        if isinstance(input_size[0], (list, tuple)):
            x = [Variable(th.rand(1, *in_size)) for in_size in input_size]
        else:
            x = Variable(th.rand(1, *input_size))

        # create properties
        summary = OrderedDict()
        hooks = []
        # register hook
        model.apply(register_hook)
        # make a forward pass
        model(x)
        # remove these hooks
        for h in hooks:
            h.remove()

        return summary


class Validator(Module):
    pass


class CallBack_PluginList(ModuleList):
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the start of an epoch.

        # Arguments
            epoch: integer, index of epoch.
            logs: dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_epoch_begin(epoch, logs)
        self._delta_t_batch = 0.
        self._delta_ts_batch_begin = deque([], maxlen=self.queue_length)
        self._delta_ts_batch_end = deque([], maxlen=self.queue_length)

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch.

        # Arguments
            epoch: integer, index of epoch.
            logs: dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_epoch_end(epoch, logs)

    def on_batch_begin(self, batch, logs=None):
        """Called right before processing a batch.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dictionary of logs.
        """
        logs = logs or {}
        t_before_callbacks = time.time()
        for callback in self.callbacks:
            callback.on_batch_begin(batch, logs)
        self._delta_ts_batch_begin.append(time.time() - t_before_callbacks)
        delta_t_median = np.median(self._delta_ts_batch_begin)
        if (self._delta_t_batch > 0. and
            delta_t_median > 0.95 * self._delta_t_batch and
                delta_t_median > 0.1):
            warnings.warn('Method on_batch_begin() is slow compared '
                          'to the batch update (%f). Check your callbacks.'
                          % delta_t_median)
        self._t_enter_batch = time.time()

    def on_batch_end(self, batch, logs=None):
        """Called at the end of a batch.

        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dictionary of logs.
        """
        logs = logs or {}
        if not hasattr(self, '_t_enter_batch'):
            self._t_enter_batch = time.time()
        self._delta_t_batch = time.time() - self._t_enter_batch
        t_before_callbacks = time.time()
        for callback in self.callbacks:
            callback.on_batch_end(batch, logs)
        self._delta_ts_batch_end.append(time.time() - t_before_callbacks)
        delta_t_median = np.median(self._delta_ts_batch_end)
        if (self._delta_t_batch > 0. and
                (delta_t_median > 0.95 * self._delta_t_batch and delta_t_median > 0.1)):
            warnings.warn('Method on_batch_end() is slow compared '
                          'to the batch update (%f). Check your callbacks.'
                          % delta_t_median)

    def on_train_begin(self, logs=None):
        """Called at the beginning of training.

        # Arguments
            logs: dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_train_begin(logs)

    def on_train_end(self, logs=None):
        """Called at the end of training.

        # Arguments
            logs: dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_train_end(logs)

    def __iter__(self):
        return iter(self.callbacks)
