class RealPythonAssertionError(AssertionError):
    def __init__(self, expected, actual, message):
        self.expected = expected
        self.actual = actual
        self.message = message or None
