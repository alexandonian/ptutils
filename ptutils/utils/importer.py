import os
import sys
import importlib


def can_import(name, package=None):
    """ Returns True if the given module can be imported.
        # Arguments
        name: str. The name of the module.
        package: str. The name of the package, if `name` is a relative import.
            This is ignored for Python versions < 3.4.
        # Return value
        If importing the specified module should succeed, returns True;
        otherwise, returns False.
    """
    try:
        importlib.util.find_spec
    except AttributeError:
        # Python < 3.4
        return importlib.find_loader(       # pylint: disable=deprecated-method
            name
        ) is not None
    else:
        # Python >= 3.4
        return importlib.util.find_spec(name, package=package) is not None


def import_name(import_name):
    """Import dotted module path and return attribute/class.


    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    import_name = str(import_name).replace(':', '.')

    try:
        module_name, class_name = import_name.rsplit('.', 1)
    except ValueError:
        raise ImportError("%s isn't a module path" % import_name)

    module = importlib.import_module(module_name)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class' %
            (module_name, class_name))


def module_dir(module):
    """Find the name of the directory that contains a module, if possible.

    Raise ValueError otherwise, e.g. for namespace packages that are split
    over several directories.

    """
    paths = list(getattr(module, '__path__', []))
    if len(paths) == 1:
        return paths[0]
    else:
        filename = getattr(module, '__file__', None)
        if filename is not None:
            return os.path.dirname(filename)
    raise ValueError('Cannot determine directory containing {}'.format(module))


def load_modules_from_path(path):
    """Import all modules from the given directory."""
    # Check and fix the path
    path += '/' if not path.endswith('/') else ''

    # Get a list of files in the directory, if the directory exists
    if not os.path.exists(path):
        raise OSError('Directory does not exist: {}'.format(path))

    # Add path to the system path and load all the files
    sys.path.append(path)
    for f in os.listdir(path):
        # Ignore anything that isn't a .py file
        if len(f) > 3 and f.endswith('.py'):
            module_name = f.rstrip('.py')
            importlib.import_module(module_name)
