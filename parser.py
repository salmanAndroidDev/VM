from exceptions import CommandTypeNotFoundError, MemorySegmentNotFoundError, \
    BadCommandError, BadCallError

from constants import CommandType, MEMORY_SEGMENTS, ARITHMETIC_OPERATIONS


class Parser:
    """
    ** Handles parsing of a single .vm file
    Read a VM command, parses the command into its lexical
    components, and provides convenient access to these components
    """

    def __init__(self, file_name):
        """ Opens the input file and gets ready to parse it """
        self.__file = open(file_name, 'r')
        self.__vm_commands = []
        self._cursor = -1
        self._clean()

    def close(self):
        if self.__file:
            self.__file.close()

    def _clean(self):
        """
            Removes comments and extra spaces from the file and put it's commands in a list
        """
        lines = self.__file.readlines()
        for line in lines:
            command = line.replace('\n', '')
            if not command.startswith('//') and command != '':
                result = command.split()
                self.__vm_commands.append(result)

    def __iter__(self):
        """Iterates through each command and adjust the cursor"""
        total_commands = len(self.__vm_commands)
        for _ in self.__vm_commands:
            self._cursor += 1
            assert 0 <= self._cursor < total_commands
            yield self

    def command_type(self):
        """ Returns a constant representing the type of the current command """
        memory_commands = ('push', 'pop')
        c_type = self.__vm_commands[self._cursor][0]

        if c_type in memory_commands:
            if c_type == 'push':
                return CommandType.C_PUSH
            return CommandType.C_POP
        elif c_type in ARITHMETIC_OPERATIONS:
            return CommandType.C_ARITHMETIC
        else:
            raise CommandTypeNotFoundError(f"{c_type} is not a good command type")

    def arg1(self):
        """Returns the first argument of the current command."""
        command = self.__vm_commands[self._cursor]  # list type
        command_type = self.command_type()

        if command_type == CommandType.C_ARITHMETIC:
            if len(command) == 1:
                return command[0]
            raise BadCommandError(f"no need to add extra argument '{command[0]}' is enough")
        elif len(command) == 3:
            if command[1] in MEMORY_SEGMENTS:
                return command[1]
            raise MemorySegmentNotFoundError(f"No memory segment with '{command[1]}' name!")
        raise BadCommandError("This command is not an appropriate vm code")

    def arg2(self):
        """ Returns the second argument of the current command. """
        appropriate_command_types = [CommandType.C_PUSH, CommandType.C_POP,
                                     CommandType.C_FUNCTION, CommandType.C_CALL]
        command = self.__vm_commands[self._cursor]  # list type
        command_type = self.command_type()

        if command_type not in appropriate_command_types:
            raise BadCallError(f"This method should not be called with '{command[0]}' command")
        if command[2].isnumeric():
            return int(command[2])
        raise ValueError('Last value is not an integer')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
