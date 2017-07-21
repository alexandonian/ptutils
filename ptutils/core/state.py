import copy

from ptutils.utils.utils import sonify


class State(dict):
    """Base module for representing module state."""

    __name__ = 'state'

    def __init__(self, *args, **kwargs):
        """Initialize State module."""
        super(State, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def state(self, *args, **kwargs):
        """Return state."""
        return self

    def load_state(self, *args, **kwargs):
        """Load state."""
        return self

    def __call__(self, *args, **kwargs):
        """Return state."""
        return self

    def __getitem__(self, name):
        """Return item `name`."""
        return dict.__getitem__(self, name)

    def __setitem__(self, name, value):
        """Set item `name` to `value`."""
        if isinstance(value, dict):
            dict.__setitem__(self, name, State(value))
        else:
            dict.__setitem__(self, name, value)

    def __delattr__(self, name):
        """Delete attribute `name`."""
        return dict.__delitem__(self, name)

    def __getattr__(self, name):
        """Return attribute `name`."""
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        """Set attribute `name` to `value`."""
        self.__setitem__(name, value)

    def __dir__(self):
        """Return dir."""
        return self.keys() + dir(dict(self))

    def __deepcopy__(self, memo):
        """Return deepcopy."""
        return State(copy.deepcopy(dict(self)))


class SonifiedState(State):
    __name__ = 'sonified_state'

    def __init__(self, *args, **kwargs):
        super(SonifiedState, self).__init__()
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __setitem__(self, name, value):
        if isinstance(name, type):
            if isinstance(value, type):
                dict.__setitem__(self, name.__name__,
                                 (sonify(name), sonify(value)))
                # dict.__setitem__(self, name.__name__, value.__name__)
            elif isinstance(value, dict):
                dict.__setitem__(self, name.__name__,
                                 (sonify(name), SonifiedState(value)))
                # dict.__setitem__(self, name.__name__, SonifiedState(value))
            else:
                dict.__setitem__(self, name.__name__,
                                 (sonify(name), sonify(value)))
                # dict.__setitem__(self, name.__name__, value)
        elif isinstance(value, type):
            dict.__setitem__(self, name, (sonify(name), sonify(value)))
            # dict.__setitem__(self, name, value.__name__)
        else:
            dict.__setitem__(self, name, (sonify(name), sonify(value)))
            # dict.__setitem__(self, name, value)
