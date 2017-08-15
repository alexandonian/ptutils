from __future__ import print_function

import abc
import collections


class AbstractBase(collections.Container):
    """Abstract Base interface."""

    __metaclass__ = abc.ABCMeta

    # def __init__(self, name=None):
    #     if name is None:
    #         name = self.__class__.__name__.lower()
    #     self._name = name
    #     self._bases = collections.OrderedDict()
    #     self._params = collections.OrderedDict()
    #     self._modules = collections.OrderedDict()
    #     self._parameters = collections.OrderedDict()

    # @abc.abstractmethod
    def to_params(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_params(cls):
        raise NotImplementedError

    def __contains__(self, item):
        return item in self._bases

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is AbstractBase:
            if (any('__contains__' in B.__dict__ for B in subclass.__mro__) and
                    any('to_params' in B.__dict__ for B in subclass.__mro__) and
                    any('from_params' in B.__dict__ for B in subclass.__mro__)):
                return True
        return NotImplementedError


class Param(dict):

    @classmethod
    def from_params(cls, **params):
        for key, value in params.items():
            if isinstance(value, collections.Mapping):
                params[key] = Param.from_params(**value)
            if isinstance(key, type):
                params[key] = (value[0].from_params(**value[1]))
            if isinstance(value, tuple):
                params[key] = (value[0].from_params(**value[1]))
        return cls(**params)


class AbstractMetaBase(AbstractBase):
    """Abstract MetaBase interface.

    The class bears no relation to python Metaclasses.
    """

    def __init__(self):
        dict.__init__(self)


class Config(AbstractMetaBase):
    pass


class State(AbstractMetaBase):
    pass


class Callback(AbstractMetaBase):
    pass


class Base(object):

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__.lower())
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
        pass

    @classmethod
    def from_params(cls, params):
        for key, value in params.items():
            if isinstance(key, type):
                if isinstance(value, collections.Mapping):
                    return key.from_params(value)
            elif isinstance(value, collections.Mapping):
                params[key] = cls.from_params(value)
        return cls(**params)

    @classmethod
    def from_params_tuple(cls, **params):
        for key, value in params.items():
            if isinstance(value, tuple):
                params[key] = (value[0].from_params_tuple(**value[1]))
        return cls(**params)

    @classmethod
    def _from_params(cls, **params):
        for key, value in params.items():
            if isinstance(key, type):
                if isinstance(value, collections.Mapping):
                    return key.from_params(**value)
            elif isinstance(value, collections.Mapping):
                params[key] = cls.from_params(**value)
        return cls(**params)

    def __setattr__(self, name, value):
        if isinstance(value, Base):
            self._bases[name] = value
        elif isinstance(value, Param):
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
        repstr = '{} ({}): ('.format(self.__class__.__name__, self._name)
        if self._bases:
            repstr += '\n'
        for name, base in self._bases.items():
            basestr = base.__repr__()
            basestr = _addindent(basestr, 2)
            repstr += '  {}\n'.format(basestr)
        repstr = repstr + ')'
        return repstr

        return self._name


def _addindent(s_, numSpaces):
    s = s_.split('\n')
    # dont do anything for single-line stuff
    if len(s) == 1:
        return s_
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

    params = {
        'name': 'mnist_trainer',
        'base': {Base: {
                'name': 'test'}},
        'my_model': {Model: {
                     'model_test': 'test'}},
        'my_datastore': {Datastore: {}},
        'my_datasource': {Datasource: {
                          'my_dataset': {Dataset: {}},
                          'name': 'poop'},
                          'another': 'damn'}}

    # params = collections.OrderedDict()

    # params['name'] = 'mnist_trainer'
    # params['base'] = {Base: {'name': 'test'}},
    # params['my_model'] = {Model: {'model_test': 'test'}},
    # params['my_datastore'] = {Datastore: {}}
    # params['my_datasource'] = {Datasource: {'my_dataset': {Dataset: {}}, 'name': 'poop'},
    #                       'another': 'damn'}

    trainer = Base.from_params(params)
    print(trainer)
    # trainer = Base.from_params_tuple(**trainer_params)
    # print(trainer)
