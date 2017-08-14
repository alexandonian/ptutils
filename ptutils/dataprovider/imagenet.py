"""Imagenet.

Primitive ImageNet Dataset and DataProvider classes.

"""
from data import Dataset
from data import DataLoader
from data import DataProvider


class ImageNetProvider(DataProvider):
    """ImageNet DataProvider class."""

    def __init__(self, ImageNet):
        super(ImageNetProvider, self).__init__()
        self.ImageNet = ImageNet

    def provide(self, mode='train'):
        self.ImageNet.mode = mode
        data_loader = DataLoader(dataset=self.ImageNet,
                                 batch_size=100,
                                 shuffle=True,
                                 pin_memory=True,
                                 num_workers=2)
        return data_loader


class ImageNet(Dataset):
    """ImageNet Dataset class."""

    _DEFAULTS = {
        'data_source': 'DEFAULT_PATH',
        # 'data_reader': HDF5DataReader,
        'transform': None,
    }

    def __init__(self, *args, **kwargs):
        super(ImageNet, self).__init__(*args, **kwargs)

        for key, value in ImageNet._DEFAULTS.items():
            if not hasattr(self, key):
                self[key] = value

    # def __init__(self, data_source, data_reader, transform=None):
    #     self.data_source = data_source
    #     self.data_reader = data_reader
    #     self.transform = transform

        # TODO: Error checking
        # self.data_dict = self.data_reader(self.data_source)
        # self.val = self.data_dict['val']
        # self.train = self.data_dict['train']
        # self.train_val = self.data_dict['train_val']
        # self.mode = self.data_dict.keys()[0]

    def __getitem__(self, index):
        """Return an (image, label) tuple given an index."""
        image = self.data_dict[self.mode]['images'][index, ...]
        label = self.data_dict[self.mode]['labels'][index, ...]

        if self.transform is not None:
            image = self.transform(image)

        return (image, label)

    def __len__(self):
        return self.data_dict[self.mode]['images'].shape[0]
