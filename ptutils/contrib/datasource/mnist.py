"""MNIST.

Primitive MNIST Dataset and DataProvider classes.

"""

import torchvision.datasets as dsets
import torchvision.transforms as transforms

from ptutils.datasource import Dataset
from ptutils.datasource import DataLoader
from ptutils.datasource import Datasource


class MNISTSource(Datasource):
    def __init__(self):
        super(MNISTSource, self).__init__()
        self.modes = ('train', 'test')
        for mode in self.modes:
            self[mode] = MNIST(root='../tests/resources/data/',
                               train=(mode == 'train'),
                               transform=transforms.ToTensor(),
                               download=True)

    def provide(self, mode='train', batch_size=100):
        return DataLoader(dataset=self[mode],
                          batch_size=batch_size,
                          shuffle=(mode == 'train'))


class MNIST(dsets.MNIST, Dataset):
    def __init__(self, root, train=True, transform=None,
                 target_transform=None, download=False):
        Dataset.__init__(self)
        super(MNIST, self).__init__(root, train, transform,
                                    target_transform, download)

    def to_params(self):
        return {name: param for name, param in self._params.items()
                if name not in ['train_data', 'train_labels',
                                'test_data', 'test_labels']}
