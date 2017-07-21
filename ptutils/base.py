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
import ptutils.core.module as module


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


class State(module.State):
    pass
# BASE = load_file('base.yml', 'yml')
# BASE_MODULES = {}
# for name, cls_ in BASE['BASE_MODULES'].items():
#     mod = type(*cls_)

#     sys.modules[__name__].__dict__[name] = mod
#     # exec('{} = type(*cls_)'.format(name))
#     BASE_MODULES[name] = mod
    # del mod


class Configuration(Module):

    def __init__(self, config=None):
        super(Configuration, self).__init__()
        self.config = config

    @classmethod
    def configure(cls, config):
        print(config)

    def __call__(self, config=None):
        if config is not None:
            return self.configure(config)
        else:
            return self.configure(self.config)


class Status(Module):

    @classmethod
    def verify(cls):
        pass


class Session(Module):

    @classmethod
    def run(self):
        pass

    def __call__(self):
        return self.run()


class Model(Module):

    def forward(self):
        pass


class Optimizer(Module):

    def step(self):
        pass

    __call__ = step


class Criterion(Module):
    pass


class Database(Module):

    @classmethod
    def access(cls):
        pass


class DataProvider(Module):

    @classmethod
    def provide(cls):
        pass


class Trainer(Module):

    @classmethod
    def train(cls):
        pass


class Tester(Module):

    @classmethod
    def test(cls):
        pass


class Runner(Module):

    @classmethod
    def run(cls):
        pass


class Saver(Module):

    @classmethod
    def save(cls):
        pass


class Loader(Module):

    @classmethod
    def load(cls):
        pass


class Serializer(Module):
    pass


class Encoder(Module):
    pass


class Decoder(Module):
    pass


class Handler(Module):
    pass


class Registry(Module):
    pass


class Plugin(Module):
    pass


class Device(Module):
    @classmethod
    def manage(cls):
        pass


class Cache(Module):
    pass


class Profiler(Module):
    pass
