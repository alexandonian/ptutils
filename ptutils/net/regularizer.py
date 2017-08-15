
from ptutils.base import Module


class Regularizer(Module):
    """Regularizer base class.
    """

    def __call__(self, x):
        return 0.

    @classmethod
    def from_config(cls, config):
        return cls(**config)


class L1L2(Regularizer):
    """Regularizer for L1 and L2 regularization.

    # Arguments
        l1: Float; L1 regularization factor.
        l2: Float; L2 regularization factor.
    """

    def __init__(self, l1=0., l2=0.):
        self.l1 = K.cast_to_floatx(l1)
        self.l2 = K.cast_to_floatx(l2)

    def __call__(self, x):
        regularization = 0.
        if self.l1:
            regularization += K.sum(self.l1 * K.abs(x))
        if self.l2:
            regularization += K.sum(self.l2 * K.square(x))
        return regularization

    def get_config(self):
        return {'l1': float(self.l1),
                'l2': float(self.l2)}
