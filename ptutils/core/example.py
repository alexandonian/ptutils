import module
import configuration


class ReadoutModule(module.Module):
    _name = 'readout_module'

    def __init__(self, name=None):
        if name is not None:
            self._name = name


class FakeAgent(module.Module):

    def __init__(self, arg, kwarg='kwarg'):
        self.arg = arg
        self.kwarg = kwarg
