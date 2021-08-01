

class CodeWriter:
    """
        Generates assembly code from the parsed VM command
    """

    def __init__(self, file):
        """
            Opens the output file / stream and get's ready to
            write into it.
        """

    def write_arithmetic(self, command):
        """
            Writes to the output file the assembly code that implements
            the given arithmetic command
        """
    def write_push_pop(self, memory_command, index):
        """
            Writes to the output file the assembly code that implements
            the given command, where command is either C_PUSH or C_POP
        """
    def close(self):
        """Closes the input file"""