from .exceptions import RealPythonAssertionError


def assert_equals(expected, actual, message=None):
    if expected != actual:
        raise RealPythonAssertionError(expected, actual, message)
