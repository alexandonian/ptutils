from __future__ import print_function

import abc
import collections


class AbstractBase(collections.Container):
    """Abstract Base interface."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None):
        if name is None:
            name = self.__class__.__name__.lower()
        self._name = name
        self._modules = collections.OrderedDict()
        self._parameters = collections.OrderedDict()

    @abc.abstractmethod
    def to_params(self):
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def from_params(cls):
        raise NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is AbstractBase:
            if (any('__contains__' in B.__dict__ for B in subclass.__mro__) and
                    any('to_params' in B.__dict__ for B in subclass.__mro__) and
                    any('from_params' in B.__dict__ for B in subclass.__mro__)):
                return True
        return NotImplemented


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
