"""Test Coordinator."""

import logging
import unittest

from ptutils.coordinator import Coordinator
from ptutils.utils.exceptions import StepError

logging.basicConfig()


class TestCoordinator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up class once before any test methods are run."""
        cls.log = logging.getLogger(':'.join([__name__, cls.__name__]))
        cls.log.setLevel('DEBUG')
        cls.test_class = Coordinator

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
        coordinator = self.test_class()
        named_coordinator = self.test_class(name='my_coordinator')
        self.assertEqual(named_coordinator._name, 'my_coordinator')
        self.log.info(coordinator._name)
        self.log.info(named_coordinator._name)

    def testStep(self):
        coordinator = self.test_class()
        self.assertEqual(coordinator.global_step, 0)
        coordinator.step()
        self.assertEqual(coordinator.global_step, 1)

        try:
            coordinator.global_step = 0
        except StepError:
            self.log.info('StepError caught.')
        else:
            raise
        try:
            coordinator.global_step = 3
        except StepError:
            self.log.info('StepError caught.')
        else:
            raise


if __name__ == '__main__':
    unittest.main()
