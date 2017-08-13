import module


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
