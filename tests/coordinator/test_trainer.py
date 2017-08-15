"""Test Trainer."""

import logging
import unittest

from ptutils.core.trainer import Trainer

logging.basicConfig()


class TestTrainer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up class once before any test methods are run."""
        cls.log = logging.getLogger(':'.join([__name__, cls.__name__]))
        cls.log.setLevel('DEBUG')
        cls.test_class = Trainer
        cls.

    @classmethod
    def tearDownClass(cls):
        """Tear down class is after all test methods have run."""
        pass

    def setUp(self):
        """Set up class before _each_ test method is executed."""
        pass

    def tearDown(self):
        """Tear Down is called after _each_ test method is executed."""
        pass

    def testInit(self):
        trainer = self.test_class()
        named_trainer = self.test_class(name='my_trainer')
        self.assertEqual(named_trainer._name, 'my_trainer')
        self.log.info(trainer._name)
        self.log.info(named_trainer._name)


if __name__ == '__main__':
    unittest.main()
