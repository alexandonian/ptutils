from __future__ import division, print_function, absolute_import

import h5py

import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.utils.data import Dataset as dset

from dataloader import DataLoader
from ptutils.base.module import Module


class DataProvider(Module):
    """Interface for all DataProvider subclasses.

    The `DataProvider` class is responsible for parsing incoming requests from
    a `ptutils.Session` and returning the appropriate data.

    To respond appropriately to requests, the `DataProvider` should manage a
    `Dataset` or collection of `Dataset`s (if a session needs to draw upon
    more than one data sources).

    Critically, a `DataProvider` subclass must implement a

        `provide`

    method that accepts an arbitrary, user-defined request for data and returns a
    valid `torch.utils.data.dataloader` object. This request can be conditioned on
    any aspect of the session's state (e.g. epoch, model accuracy, etc.).

    A `torch.utils.data.dataloader combines a `Dataset` and a `Sampler`, and provides
    single- or multi-process iterators over the dataset. In constructing a dataloader,
    you are free to specify parameters such as batch size, data sampling strategies and the number of
    subprocesses to use for data loading.
    See http://pytorch.org/docs/data.html for more details.

    """

    __name__ = 'dataprovider'

    def __init__(self, *args, **kwargs):
        super(DataProvider, self).__init__(*args, **kwargs)

    def provide(self):
        """Return a `torch.utils.data.dataloader` given an arbitrary data request."""
        raise NotImplementedError

    def __call__(self):
        return self.provide()


class Dataset(Module, dset):
    """Interface for all Dataset subclasses.

    This class simply extends Pytorch's Dataset class to be able to load data
    in different formats by introducing the notion of a `DataReader` and
    `transform`.
    """

    __name__ = 'dataset'

    def __init__(self, *args, **kwargs):
        super(Dataset, self).__init__(*args, **kwargs)
        self.data_source = None
        self.data_reader = None
        self.transform = None

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


class DataReader(Module):
    """Interface for DataReader subclasses (e.g. HDF5, TFRecords, etc.).

    - Reads data of a specified format efficiently.
    - Exists completely independent of anything ptutils related.
        (Can use is just to read single data file, if desired.)

    """

    def __init__(self):
        super(DataReader, self).__init__()

    def read(self, *data_source):
        """Load data from `data_source` into a dictionary of array-like objects.

        The structure of the data dictionary should reflect intrinsic structure
        of the data source (e.g., if a dataset is partitioned into distinct sets
        such as train/val and testing data, data_dict.keys() should relfect this.
        The `Dataset` class will be responsible for parsing this dict.

        Should be overriden by all subclasses.

        """
        raise NotImplementedError()

    def __call__(self, *data_source, **kwargs):
        data_dict = self.read(*data_source, **kwargs)
        return data_dict


class HDF5DataReader(DataReader):
    """Return an HDF5 file object given a path to an HDF5 file."""

    def __init__(self):
        super(HDF5DataReader, self).__init__()
        self.data_dict = None

    def read(self, hdf5_file_path):
        self.data_dict = h5py.File(hdf5_file_path, 'r')
        return self.data_dict


class TFRecordReader(DataReader):
    def __init__(self):
        self.data_dict = None

    def read(self, tfrecord_path):
        rec_iter = tf.python_io.tf_record_iterator(path=tfrecord_path)
        datum = tf.train.Example()

        # TODO: iterate of records
        # TODO: insert each datum into a torch tensor
        for rec in rec_iter:
            datum.ParseFromString(rec)
            data_str = (datum.features.feature['images'].bytes_list.value[0])
            img_1d = np.fromstring(data_str, dtype=np.uint8)
            img = img_1d.reshape((160, 375, -1))
