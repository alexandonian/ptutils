from __future__ import print_function

import os
import logging
import unittest
from collections import OrderedDict

from ptutils import constants
from ptutils.core import module, state


@unittest.skip('Skipping TestConfiguration')
class TestModule(unittest.TestCase):

    _class = module.Module
    test_types = {
        # Numeric types
        'test_int': int(),
        'test_long': long(),
        'test_float': float(),
        'test_complex': complex(),

        # Sequence types,
        'test_str': str(),
        'test_set': set(),
        'test_list': list(),
        'test_tuple': tuple(),
        'test_range': range(1),
        'test_xrange': xrange(1),
        'test_unicode': unicode(),
        'test_bytearray': bytearray(),
        'test_frozenset': frozenset(),
        'test_buffer': buffer('test_buffer'),

        # Mapping types,
        'test_dict': dict(),

        # Other built-in types,
        'test_module': os,
        'test_none': None,
        'test_bool': True,
        'test_type': type,
        'test_function': lambda x: x,
        'test_class': type(str(), tuple(), dict()),
        'test_obj': type(str(), tuple(), dict())(),
        'test_obj': type('TestClass', (object,), {'method': lambda self: self})(),
        'test_method': type(str(), tuple(), {'method': lambda self: self}).method,
    }

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

    @classmethod
    def setUpClass(cls):
        """setUpClass is called once for each class before any tests are run."""

    @classmethod
    def tearDownClass(cls):
        """tearDownClass is called once for each class before any tests are run."""
        pass

    def setUp(self):
        """setUp is called before _each_ test method is executed."""
        self.module = self._class()

    def tearDown(self):
        """tearDown is called after _each_ test method is executed."""
        pass

    def test_init(self):
        mod = base.Module()
        self.assertTrue(hasattr(mod, '_state'))
        self.assertTrue(hasattr(mod, '_modules'))
        self.assertTrue(hasattr(mod, '_properties'))
        self.assertIsInstance(mod._state, state.State)
        self.assertIsInstance(mod._modules, OrderedDict)
        self.assertIsInstance(mod._properties, OrderedDict)

        for key, value in self.test_types.items():
            self.assertIsInstance(base.Module(value), base.Module)

    def test_base_class_type(self):
        self.assertEqual(base.Module.__base__, module.Module)

    def test_base_class_name(self):
        self.assertEqual(base.Module.__base__.__name__,
                         constants.BASE['MODULE']['NAME'])

    def test_class_name(self):
        self.assertEqual(base.Module.__name__,
                         constants.BASE['MODULE']['NAME'])

    def test_register_module(self):
        self.module.register_module('submodule', self._class())
        self.assertEqual(self.module.submodule, self.module._MODULE)

    def test_setattr_module(self):
        pass

    def test_setattr_property(self):
        pass

    def test_getattr_module(self):
        pass

    def test_getattr_property(self):
        pass

    def test_getitem_module(self):
        pass

    def test_getitem_property(self):
        pass

    def test_setitem_module(self):
        pass


@unittest.skip('Skipping TestConfiguration')
class TestConfiguration(TestModule):

    def setUp(self):
        """setUp is called before _each_ test method is executed."""
        pass

    def tearDown(self):
        """tearDown is called after _each_ test method is executed."""
        pass

    def test_init(self):
        super(TestConfiguration, self).test_init()
        base_c = base.Configuration()
        int_c = base.Configuration(self.test_types['test_int'])
        assert(isinstance(base_c, base.Module))
        assert(isinstance(int_c, base.Module))


@unittest.skip('Skipping TestState')
class TestState(TestModule):

    def test_init(self):
        state = base.State()


if __name__ == '__main__':
    unittest.main()
