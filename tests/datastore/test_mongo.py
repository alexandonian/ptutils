"""Test MongoDatastore."""

import logging
import unittest

from ptutils.datastore import MongoDatastore

logging.basicConfig()


class TestMongoDatastore(unittest.TestCase):

    DEFALUT_NAME = 'my_mongo_datastore'
    DEFAULT_PORT = 27017
    DEFAULT_HOSTNAME = 'localhost'
    DEFAULT_DATABASE_NAME = 'TestMongoDatastore_Database'
    DEFAULT_COLLECTION_NAME = 'TestMongoDatastore_Collection'

    @classmethod
    def setUpClass(cls):
        """Set up class once before any test methods are run."""
        cls.log = logging.getLogger(':'.join([__name__, cls.__name__]))
        cls.log.setLevel('DEBUG')

        cls.test_class = MongoDatastore
        cls.test_config = {'database_name': cls.DEFAULT_DATABASE_NAME,
                           'collection_name': cls.DEFAULT_COLLECTION_NAME,
                           'hostname': cls.DEFAULT_HOSTNAME,
                           'port': cls.DEFAULT_PORT}

    @classmethod
    def tearDownClass(cls):
        """Tear down class is after all test methods have run."""
        pass

    def setUp(self):
        """Set up class before each test method is executed."""
        pass

    def tearDown(self):
        """Tear Down is called after each test method is executed."""
        pass

    def testInit(self):
        mongo_datastore = self.test_class(**self.test_config)
        named_mongo_datastore = self.test_class(name=self.DEFALUT_NAME,
                                                **self.test_config)
        self.assertEqual(named_mongo_datastore._name, self.DEFALUT_NAME)
        self.log.info(mongo_datastore)
        self.log.info(named_mongo_datastore)
        self.log.info(mongo_datastore._name)
        self.log.info(mongo_datastore.database)
        self.log.info(named_mongo_datastore._name)


if __name__ == '__main__':
    unittest.main()
