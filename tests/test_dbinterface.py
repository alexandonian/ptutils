import sys
import copy
import pymongo
import unittest

from ptutils.datastore import Key, Query
from ptutils.database import MongoInterface
from ptutils.datastore.mongo import MongoDatastore


class TestDatastore(unittest.TestCase):
    pkey = Key('/dfadasfdsafdas/')
    stores = []
    num_elem = []

    def check_length(self,len):
        try:
            for sn in self.stores:
                self.assertEqual(len(sn), len)
        except TypeError, e:
            pass

    def subtest_remove_nonexistent(self):
        self.assertTrue(len(self.stores) > 0)
        self.check_length(0)

        # ensure removing non-existent keys is ok.
        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                self.assertFalse(sn.contains(key))
                sn.delete(key)
                self.assertFalse(sn.contains(key))

        self.check_length(0)

    def subtest_insert_elems(self):
        # insert num_elem elems
        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                self.assertFalse(sn.contains(key))
                sn.put(key, value)
                self.assertTrue(sn.contains(key))
                self.assertEqual(sn.get(key), value)

        # reassure they're all there.
        self.check_length(self.num_elem)

        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                self.assertTrue(sn.contains(key))
                self.assertEqual(sn.get(key), value)

        self.check_length(self.num_elem)

    def check_query(self, query, total, slice):
        allitems = list(range(0, total))
        resultset = None

        for sn in self.stores:
            try:
                contents = list(sn.query(Query(self.pkey)))
                expected = contents[slice]
                resultset = sn.query(query)
                result = list(resultset)

                # make sure everything is there.
                self.assertTrue(len(contents) == len(allitems),\
                    '%s == %s' %  (str(contents), str(allitems)))
                self.assertTrue(all([val in contents for val in allitems]))

                self.assertTrue(len(result) == len(expected),\
                    '%s == %s' %  (str(result), str(expected)))
                self.assertTrue(all([val in result for val in expected]))

                #TODO: should order be preserved?
                #self.assertEqual(result, expected)

            except NotImplementedError:
                print 'WARNING: %s does not implement query.' % sn

        return resultset

    def subtest_queries(self):
        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                sn.put(key, value)

        k = self.pkey
        n = int(self.num_elem)

        self.check_query(Query(k), n, slice(0, n))
        self.check_query(Query(k, limit=n), n, slice(0, n))
        self.check_query(Query(k, limit=n/2), n, slice(0, n/2))
        self.check_query(Query(k, offset=n/2), n, slice(n/2, n))
        self.check_query(Query(k, offset=n/3, limit=n/3), n, slice(n/3, 2*(n/3)))
        del k
        del n

    def subtest_update(self):
        # change num_elem elems
        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                self.assertTrue(sn.contains(key))
                sn.put(key, value + 1)
                self.assertTrue(sn.contains(key))
                self.assertNotEqual(value, sn.get(key))
                self.assertEqual(value + 1, sn.get(key))

        self.check_length(self.num_elem)

    def subtest_remove(self):
        # remove num_elem elems
        for value in range(0, self.num_elem):
            key = self.pkey.child(value)
            for sn in self.stores:
                self.assertTrue(sn.contains(key))
                sn.delete(key)
                self.assertFalse(sn.contains(key))

        self.check_length(0)

    def subtest_simple(self, stores, num_elem=1000):
        self.stores = stores
        self.num_elem = num_elem

        self.subtest_remove_nonexistent()
        self.subtest_insert_elems()
        self.subtest_queries()
        self.subtest_update()
        self.subtest_remove()


class TestMongoDatastore(TestDatastore):

    def setUp(self):
        self.dbinterface = MongoInterface(db_name='dbinterface_testdb',
                                          collection_name='testcol')
        self.conn = pymongo.MongoClient()
        self.conn.drop_database('datastore_testdb')

    def tearDown(self):
        self.conn.drop_database('datastore_testdb')
        self.conn.drop_database('dbinterface_testdb')
        del self.conn

    @unittest.skip('skipping')
    def test_mongo(self):
        ms = MongoDatastore(self.conn.datastore_testdb)
        self.subtest_simple([ms], num_elem=500)

    def test_query(self):
        ms = MongoDatastore(self.conn.datastore_testdb)
        pk = Key('exp_id')

        train_key = pk.instance('train')
        train_val = {'key': str(train_key), 'name': 'vgg', 'step': 50, 'loss': 1.0}
        ms.put(train_key, train_val)
        self.dbinterface.save(copy.copy(train_val))

        test_key = pk.instance('test')
        test_val = {'key': str(test_key), 'name': 'vgg_test', 'step': 100, 'loss': 2.0}
        ms.put(test_key, test_val)
        self.dbinterface.save(copy.copy(test_val))


        res = list(ms.query(Query(pk).filter('step', '<', 75).filter('loss', '<', 1.5)))
        assert res == [train_val]

        q = {'step': {'$lt': 75}, 'loss': {'$lt': 1.5}}
        res = self.dbinterface.load(q)
        print(res)

        res = list(ms.query(Query(pk).filter('step', '>', 75)))
        assert res == [test_val]
        print(res)

        res = list(ms.query(Query(pk).filter('name', '!=', 'vgg')))
        assert res == [test_val]
        print(res)


if __name__ == '__main__':
    unittest.main()
