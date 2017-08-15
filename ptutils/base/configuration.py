from collections import OrderedDict

import module
from ptutils.base.state import State
from ptutils.utils.utils import parse_config

class Configuration(module.Module):
    """Configure a module or group of modules from a Configuration state.

    A Configuration module is a dictionary that specifies the configuration of
    its parent module.

    """

    __name__ = 'configuration'

    def __init__(self, config):
        """Initialize Configuration module."""
        super(Configuration, self).__init__()

        config_dict = parse_config(config)

        self._state = State(config_dict)
        self._configs = OrderedDict()

        for key, value in config_dict.items():
            if isinstance(key, type):
                if isinstance(value, dict):
                    name = key.__dict__.get('__name__', key.__name__)
                    self._configs[name] = (key, Configuration(value))
            elif isinstance(value, dict):
                key, value = self._find_configs(value)
                if isinstance(value, dict):
                    name = key.__dict__.get('__name__', key.__name__)
                    self._configs[name] = (key, Configuration(value))
            else:
                self[key] = value
        self.configure()

    def configure(self):
        for name, (cls_, config) in self._configs.items():
            config.configure()
            self[name] = cls_(**config._state)
        return self


    def __call__(self):
        self.configure()

    def __repr__(self):
        return self._state.__repr__()

    def _find_configs(self, dict_):
        for key, value in dict_.items():
            if isinstance(key, type):
                return key, value
            if isinstance(value, dict):
                key, value = self._find_configs(value)
        return key, value

    def _parse(self, config):
        if isinstance(config, str):
            pattern = r'.(yml|yaml|json|pkl)$'
            m = re.search(pattern, config, flags=re.I)
            if m is not None:
                ext = m.group().lower()

class Mod(module.Module):
    def __init__(self, config):
        """Initialize Configuration module."""
        super(Config, self).__init__()

        config_dict = parse_config(config)

        self._state = State(config_dict)
        self._configs = OrderedDict()

        for key, value in config_dict.items():
            if isinstance(key, type):
                if isinstance(value, dict):
                    name = key.__dict__.get('__name__', key.__name__)
                    self._configs[name] = (key, Configuration(value))
            elif isinstance(value, dict):
                key, value = self._find_configs(value)
                if isinstance(value, dict):
                    name = key.__dict__.get('__name__', key.__name__)
                    self._configs[name] = (key, Configuration(value))
            else:
                self[key] = value
        self.configure()

    def configure(self):
        for name, (cls_, config) in self._configs.items():
            config.configure()
            self[name] = cls_(**config._state)
        return self