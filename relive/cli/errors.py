
class InvalidArgumentType(Exception):
    """Exception raised for mismatching argument type.
    """

    def __init__(self, message):
        self.message = 'Expected: ' + message
        super().__init__(self.message)


class MissingArgument(Exception):
    """Exception raised for missing arguments.
    """

    def __init__(self, argument):
        self.message = argument
        super().__init__(self.message)
