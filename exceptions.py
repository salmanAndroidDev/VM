"""
    Custom Exceptions that should be raised when parsing and translating
    VM commands.
"""


class CommandTypeNotFoundError(ValueError):
    """This exception is raised when command name is not found"""
    pass


class MemorySegmentNotFoundError(ValueError):
    """This exception is raised when given memory segment is not found"""
    pass


class BadCommandError(ValueError):
    """This exception is raised when given command is bad written"""
    pass


class BadCallError(ValueError):
    """This exception is raised when calling an unappropriate method"""
    pass
