import torch.nn as nn

from ptutils.base import Base


class Net(nn.Module, Base):

    def __init__(self, *args, **kwargs):
        super(Net, self).__init__()
        Base.__init__(self, *args, **kwargs)
        for arg in args:
            if isinstance(arg, nn.Module):
                # self.__setattr__(type(arg), arg)
                self = arg

    # def to_params(self):
    #     params = {}
    #     for name, value in self.__dict__.items():
    #         if not name.startswith('_'):
    #             params[name] = value
    #     # for name, mod in self._modules.items():
    #     try:
    #         for name, mod in self.modules():
    #             net = Net(mod)
    #             params[name] = net.to_params()
    #     except Exception as e:
    #         print(e)
    #     try:
    #         for name, mod in self.children():
    #             net = Net(mod)
    #             params[name] = net.to_params()
    #     except Exception as e:
    #         print(e)
    #     return params

    def __setattr__(self, name, value):
        if isinstance(value, nn.Module):
            self._bases[name] = value
        super(Net, self).__setattr__(name, value)


class MNIST(Net):
    __name__ = 'MNIST'

    def __init__(self,):
        super(MNIST, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.fc = nn.Linear(7 * 7 * 32, 10)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


# m = MNIST()
# conv = m.layer1[0]
# cn = Net(conv)
# print(cn.to_params())
