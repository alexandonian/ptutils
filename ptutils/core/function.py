from abc import ABCMeta


class FunctionMeta(ABCMeta):
        """Function metaclass.

    This metaclass sets up the following properties:
        _is_legacy: True if forward is not defined as a static method.
        _backward_cls: The Function class corresponding to the differentiated
            version of this function (which is generated on the fly by this
            metaclass).
    """

    def __init__(cls, name, bases, attrs):
        for super_cls in cls.mro():
            forward = super_cls.__dict__.get('forward')
            if forward is not None:
                has_static_forward = isinstance(forward, staticmethod) or isinstance(forward, classmethod)
                break

        setattr(cls, '_is_legacy', not has_static_forward)

        # old-style functions
        if not has_static_forward:
            return super(FunctionMeta, cls).__init__(name, bases, attrs)

        backward_fn = type(name + 'Backward', (BackwardCFunction,), {'_forward_cls': cls})
        setattr(cls, '_backward_cls', backward_fn)

        return super(FunctionMeta, cls).__init__(name, bases, attrs)

class Function(with_metaclass(FunctionMeta, _C._FunctionBase, _ContextMethodMixin, _HookMixin)):
    """Records operation history and defines formulas for differentiating ops.

    Every operation performed on :class:`Variable` s creates a new function
    object, that performs the computation, and records that it happened.
    The history is retained in the form of a DAG of functions, with edges
    denoting data dependencies (``input <- output``). Then, when backward is
    called, the graph is processed in the topological ordering, by calling
    :func:`backward` methods of each :class:`Function` object, and passing
    returned gradients on to next :class:`Function` s.

    Normally, the only way users interact with functions is by creating
    subclasses and defining new operations. This is a recommended way of
    extending torch.autograd.

    Since Function logic is a hotspot in most scripts, almost all of it
    was moved to our C backend, to ensure that the framework overhead is
    minimal.

    Each function is meant to be used only once (in the forward pass).

    Attributes:
        saved_tensors: Tuple of Tensors that were saved in the call to
            :func:`forward`.
        saved_variables: Tuple of Variables that correspond to the tensors
            saved in the call to :func:`forward`.
        needs_input_grad: Tuple of booleans of length :attr:`num_inputs`,
            indicating whether a given input requires gradient. This can be
            used to optimize buffers saved for backward, and ignoring gradient
            computation in :func:`~Function.backward`.
        num_inputs: Number of inputs given to :func:`forward`.
        num_outputs: Number of tensors returned by :func:`forward`.
        requires_grad: Boolean indicating whether the :func:`backward` will
            ever need to be called.
    """

    # only for backward compatibility
    __call__ = _C._FunctionBase._do_forward

    @staticmethod
    def forward(*args, **kwargs):
        """Performs the operation.

        This function is to be overriden by all subclasses.

        It can take and return an arbitrary number of tensors.
        """
        raise NotImplementedError

    @staticmethod
    def backward(*grad_outputs):
        """Defines a formula for differentiating the operation.

        This function is to be overriden by all subclasses.

        All arguments are tensors. It has to accept exactly as many arguments,
        as many outputs did :func:`forward` return, and it should return as
        many tensors, as there were inputs to :func:`forward`. Each argument
        is the gradient w.r.t the given output, and each returned value should
        be the gradient w.r.t. the corresponding input.
        """
        raise NotImplementedError

class