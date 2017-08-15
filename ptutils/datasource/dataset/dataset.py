from __future__ import division, print_function, absolute_import

from ptutils.base import Base

class Dataset(Base):
    """An abstract class representing a Dataset.

    All other datasets should subclass it. All subclasses should override
    ``__len__``, that provides the size of the dataset, and ``__getitem__``,
    supporting integer indexing in range from 0 to len(self) exclusive.

    """

    def __getitem__(self, index):
        """Must return a data item given an index in [0, 1, ..., self.__len__()].

        Recommended implementation:

        1. Using `self.data_loader`, read data from `self.data_source` efficiently.
        2. Preprocess the data using `self.preprocessor`.
        3. Return a data item (e.g. image and label)
        """
        raise NotImplementedError()

    def __len__(self):
        """Return the total size (length) of you dataset."""
        raise NotImplementedError()
