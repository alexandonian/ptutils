"""CIFAR.

Primitive CIFAR Dataset and DataProvider classes.

"""

import torchvision.datasets as dsets
import torchvision.transforms as transforms

from datasource import DataLoader
from datasource import DataProvider


class CIFARProvider(DataProvider):
    def __init__(self):
        super(CIFARProvider, self).__init__()
        self.modes = ('train', 'test')
        self.datasets = {'CIFAR10': {}, 'CIFAR100': {}}
        for mode in self.modes:
            self.datasets['CIFAR10'][mode] = dsets.CIFAR10(root='../tests/resources/data/',
                                                           train=(mode == 'train'),
                                                           transform=transforms.ToTensor(),
                                                           download=True)
            self.datasets['CIFAR100'][mode] = dsets.CIFAR100(root='../tests/resources/data/',
                                                             train=(mode == 'train'),
                                                             transform=transforms.ToTensor(),
                                                             download=True)

    def provide(self, dataset='CIFAR10', mode='train', batch_size=100):
        return DataLoader(dataset=self.datasets[dataset][mode],
                          batch_size=batch_size,
                          pin_memory=True,
                          shuffle=(mode == 'train'))
