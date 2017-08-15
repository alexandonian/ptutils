from ptutils.base import Base


class Criterion(Base):
    __name__ = 'criterion'

    def __init__(self, criterion):
        super(Criterion, self).__init__()
        self.criterion = criterion()
        self.__name__ = criterion.__name__

    def __call__(self, *args, **kwargs):
        return self.criterion(*args, **kwargs)

    def __repr__(self):
        return self.__name__
