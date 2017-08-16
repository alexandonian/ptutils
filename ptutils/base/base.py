from __future__ import print_function

import copy
import logging
import collections
from pprint import pprint as print

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel('DEBUG')


class Base(object):

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', type(self).__name__.lower())
        self._bases = collections.OrderedDict()
        self._params = collections.OrderedDict()

        for i, arg in enumerate(args):

            if isinstance(arg, Base):
                self.__setattr__(arg._name, arg)

            if isinstance(arg, collections.Mapping):
                for key, value in arg.items():
                    setattr(self, key, value)

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def to_params(self):
        params = {}
        for name, param in self._params.items():
            if param is not None:
                params[name] = param
        for name, base in self._bases.items():
            try:
                params[name] = base.to_params()
            except AttributeError as error:
                log.warning(error)
                try:
                    params[name] = base.state_dict().keys()
                except AttributeError as error:
                    log.warning(error)
        return params

    @classmethod
    def from_params(cls, params):
        for key, value in params.items():
            if isinstance(key, type):
                if isinstance(value, collections.Mapping):
                    return key.from_params(value)
            elif isinstance(value, collections.Mapping):
                params[key] = cls.from_params(value)
        # params['_params'] = copy.copy(params)
        return cls(**params)

    def __setattr__(self, name, value):
        if isinstance(value, Base):
            self._bases[name] = value
        else:
            if not name.startswith('_'):
                self._params[name] = value
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name in self._bases:
            return self._bases[name]
        elif name in self._params:
            return self._params[name]
        elif name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError("'{}' object has no attribute '{}'"
                                 .format(type(self).__name__, name))

    def __setitem__(self, name, item):
        self.__setattr__(name, item)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __repr__(self):
        """Return module string representation."""
        repstr = '{} ({}): ('.format(type(self).__name__, self._name)
        if self._bases:
            repstr += '\n'
        for name, base in self._bases.items():
            basestr = base.__repr__()
            basestr = _addindent(basestr, 2)
            repstr += '  {}\n'.format(basestr)
        repstr = repstr + ')'
        return repstr

    @classmethod
    def from_params_tuple(cls, **params):
        for key, value in params.items():
            if isinstance(value, tuple):
                params[key] = (value[0].from_params_tuple(**value[1]))
        return cls(**params)

    @classmethod
    def _from_params(cls, **params):
        """Attempt to use ** syntax."""
        for key, value in params.items():
            if isinstance(key, type):
                if isinstance(value, collections.Mapping):
                    return key.from_params(**value)
            elif isinstance(value, collections.Mapping):
                params[key] = cls.from_params(**value)
        return cls(**params)


def _addindent(string, numSpaces):
    s = string.split('\n')
    # dont do anything for single-line stuff
    if len(s) == 1:
        return string
    first = s.pop(0)
    s = [(numSpaces * ' ') + line for line in s]
    s = '\n'.join(s)
    s = first + '\n' + s
    return s


if __name__ == '__main__':
    Model = type('Model', (Base,), {})
    Datastore = type('Datastore', (Base,), {})
    Datasource = type('Datasource', (Base,), {})
    Dataset = type('Dataset', (Base,), {})

    # PARAMS FORMAT 1: attr_name: (sub_base_class, sub_base_params)
    trainer_params = {
        'name': 'mnist_trainer',
        'base': (
            Base,
            {'name': 'test'}),
        'my_model': (
            Model,
            {'test': 'test'}),
        'my_datastore': (Datastore, {}),
        'my_datasource': (
            Datasource,
            {'my_dataset': (
                Dataset, {'name': 'MNIST'})})}

    # PARAMS FORMAT 2: attr_name: {sub_base_class: {sub_base_params}}
    params = {
        'name': 'mnist_trainer',
        'base': {Base: {
                'name': 'test'}},
        'my_model': {Model: {
                     'model_test': 'test'}},
        'my_datastore': {Datastore: {}},
        'my_datasource': {Datasource: {
                          'my_dataset': {Dataset: {}},
                          'name': 'mnist_dataset'},
                          'another': 'test'}}

    {'func': Model,
    ''}
    trainer = Base.from_params(params)
    print(trainer)
    print(trainer.to_params())

    # print(Base(trainer))

    trainer_tuple = Base.from_params_tuple(**trainer_params)
    print(trainer_tuple)
