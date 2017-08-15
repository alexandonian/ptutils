"""PTutils exeptions.

Global PTutils exception and warning classes.

"""


class StepError(Exception):
    """Exception class to raise if step is not incremented."""

class ConfigurationError(Exception):
    """Exception class to raise if a Configurable object has an issue."""

    pass


class NotFoundError(Exception):
    """Exception class to raise if a file was not found."""

    pass


class EstimatorNotTrainedError(Exception):
    """Exception class to raise if estimator is used before being trained."""

    pass


class ModuleNotBuiltError(Exception):
    """Exception class to raise if graph module is used before being built."""

    pass
