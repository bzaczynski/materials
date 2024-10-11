class RealPythonException(Exception):
    pass


class RealPythonAssertionError(AssertionError):
    def __init__(self, expected, actual, message):
        self.expected = expected
        self.actual = actual
        if message:
            self.message = message.rstrip(".:") + "."
        else:
            self.message = None
