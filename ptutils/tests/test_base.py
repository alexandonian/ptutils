from __future__ import print_function

import os
import logging
import unittest

from ptutils.base import Module, Configuration


class TestModule(unittest.TestCase):

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

    def test_init(self):
        self.logger.info('try again...')
        self.assertIsInstance(Module(), Module)
        for key, value in self.test_types.items():
            self.assertIsInstance(Module(value), Module)


class TestConfiguration(TestModule):

    def setUp(self):
        """setUp is called before _each_ test method is executed."""
        pass

    def tearDown(self):
        """tearDown is called after _each_ test method is executed."""
        pass

    def test_init(self):
        base_c = Configuration()
        int_c = Configuration(self.test_types['test_int'])
        assert(isinstance(base_c, Module))
        assert(isinstance(int_c, Module))


if __name__ == '__main__':
    unittest.main()
    # def test_return_true(self):
    #     a = A()
    #     assert_equal(a.return_true(), True)
    #     assert_not_equal(a.return_true(), False)

    # def test_raise_exc(self):
    #     a = A()
    #     assert_raises(KeyError, a.raise_exc, "A value")

    # @raises(KeyError)
    # def test_raise_exc_with_decorator(self):
    #     a = A()
    #     a.raise_exc("A message")


