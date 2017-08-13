"""Base Datastore module."""


class Datastore(object):
    """A Datastore represents storage for any key-value pair.

    Datastores are general enough to be backed by all kinds of different storage:
    in-memory caches, databases, a remote datastore, flat files on disk, etc.

    The general idea is to wrap a more complicated storage facility in a simple,
    uniform interface, keeping the freedom of using the right tools for the job.
    In particular, a Datastore can aggregate other datastores in interesting ways,
    like sharded (to distribute load) or tiered access (caches before databases).

    While Datastores should be written general enough to accept all sorts of
    values, some implementations will undoubtedly have to be specific (e.g. SQL
    databases where fields should be decomposed into columns), particularly to
    support queries efficiently.

    """

    # Core API. Datastore mplementations MUST implement these methods.

    def get(self, key):
        """Return the object named by key or None if it does not exist.

        None takes the role of default value, so no KeyError exception is raised.

        Args:
            key: Key naming the object to retrieve

        Returns:
            object or None

        """
        raise NotImplementedError

    def put(self, key, value):
        """Store the object `value` named by `key`.

        How to serialize and store objects is up to the underlying datastore.
        It is recommended to use simple objects (strings, numbers, lists, dicts).

        Args:
            key: Key naming `value`
            value: the object to store.

        """
        raise NotImplementedError

    def delete(self, key):
        """Remove the object named by `key`.

        Args:
            key: Key naming the object to remove.
        """
        raise NotImplementedError

    def query(self, query):
        """Return an iterable of objects matching criteria expressed in `query`.

        Implementations of query will be the largest differentiating factor
        amongst datastores. All datastores **must** implement query, even using
        query's worst case scenario, see :ref:class:`Query` for details.

        Args:
            query: Query object describing the objects to return.

        Raturns:
            iterable cursor with all objects matching criteria
        """
        raise NotImplementedError

    # Secondary API. Datastores MAY provide optimized implementations.

    def contains(self, key):
        """Return whether the object named by `key` exists.

        The default implementation pays the cost of a get. Some datastore
        implementations may optimize this.

        Args:
            key: Key naming the object to check.

        Returns:
            boolean whether the object exists
        """
        return self.get(key) is not None


class NullDatastore(Datastore):
    """A Null datastore stores nothing, but conforms to the API."""

    def get(self, key):
        """Return the object named by key or None if it does not exist (None)."""
        return None

    def put(self, key, value):
        """Store the object `value` named by `key (does nothing)."""
        pass

    def delete(self, key):
        """Remove the object named by `key` (does nothing)."""
        pass

    def query(self, query):
        """Return an iterable of objects matching criteria in `query` (empty)."""
        return query([])


class DictDatastore(Datastore):
    """Simple in-memory datastore backed by nested dicts."""

    def __init__(self):
        self._items = dict()

    def _collection(self, key):
        """Return the namespace collection for `key`."""
        collection = key
        if collection not in self._items:
            self._items[collection] = dict()
        return self._items[collection]

    def get(self, key):
        """Return the object named by `key` or None.

        Retrieves the object from the collection corresponding to `key`.

        Args:
            key: Key naming the object to retrieve.

        Returns:
            object or None

        """
        try:
            return self._collection(key)[key]
        except KeyError:
            return None

    def put(self, key, value):
        """Store the object `value` named by `key`.

        Args:
            key: Key naming `value`
            value: the object to store.

        """
        if value is None:
            self.delete(key)
        else:
            self._collection(key)[key] = value

    def delete(self, key):
        """Remove the object named by `key`.

        Args:
            key: Key naming the object to remove.

        """
        try:
            del self._collection(key)[key]
        except KeyError:
            pass
        else:
            if len(self._collection(key)) == 0:
                del self._items[key]

    def contains(self, key):
        """Return whether the object named by `key` exists.

        Checks for the object in the collection corresponding to `key`.

        Args:
            key: Key naming the object to check.key

        Returns:
            boolean: whether the object exists

        """
        return key in self._collection(key)

    def query(self, query):
        """Return an iterable of objects matching criteria expressed in `query`.

        Args:
            query: Query object describing the objects to return.

        Returns:
            iterable: cursor with all objects matching criteria.

        """
        if query in self._items:
            return query(self._items[query].values())
        else:
            return query([])
