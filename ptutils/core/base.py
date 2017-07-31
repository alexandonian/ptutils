import collections
from collections import OrderedDict
from abc import ABCMeta, abstractmethod, abstractproperty


class Module(collections.Container):
    __metaclass__ = ABCMeta

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            self._name = self.__class__.__name__.lower()
        self._state = OrderedDict()
        self._modules = OrderedDict()

    @abstractmethod
    def state_dict(self):
        return self._state

    @classmethod
    @abstractmethod
    def load_state_dict(cls, state):
        pass

    @abstractproperty
    def _state(self):
        pass

    @abstractproperty
    def _config(self):
        pass

    @abstractproperty
    def _modules(self):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Data:
            if any("__contains__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class MetaModule(Module):
    """Base MetaModule which should be used to configure, handle and modules.

    (no relation to python Metaclasses)
    """

    def __init__(self):
        self.module = module
        self.config = config
        self.status = status

        self.saver = saver
        self.loader = loader
        self.summarizer = summarizer


# class Module(Data, collections.Callable):

#     def __init__(self, name=None, *args, **kwargs):
#         if not name:
#             self.name = self.__class__.__name__.lower()


# class MyData(Data):

#     def __init__(self, data):
#         self.data = data

#     def __contains__(self, item):
#         return self.data.__contains__(item)

# class MyModule(Module):

#     def __init__(self, data, func):
#         self.data = data
#         self.func = func

#     def __contains__(self, item):
#         return self.data.__contains__(item)

#     def __call__(self, input):
#         return self.func(input)

# d = MyData([1, 2, 3])
# m = MyModule([1, 2, 3], type)

# print(1 in m)
# print(m(m.data))
