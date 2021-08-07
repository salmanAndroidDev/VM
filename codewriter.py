from constants import ARITHMETIC_OPERATIONS, MEMORY_SEGMENTS, segment_pointers, C_PUSH, C_POP
from parser import CommandType


class CodeWriter:
    """
        Generates assembly code from the parsed VM command
    """

    def __init__(self, file_name):
        """ Opens the output file and gets ready to write into it."""
        self.file_name = file_name
        self.file = open(file_name, 'w')
        self.__asm_code = []

    def write_arithmetic(self, operation):
        """
            Writes to the output file the assembly code that implements
            the given arithmetic command
        """
        assert operation in ARITHMETIC_OPERATIONS
        print(operation)

    def __translate_add(self):
        """Translate addition arithmetic command"""
        assembly_commands = ['@SP',  # SP -= 2;
                             'M=M-1',
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             '@SP',  # SP++;
                             'M=M+1',
                             'A=M',  # SP = M+D
                             'M=M+D'
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_sub(self):
        """Translate subtraction arithmetic command"""
        assembly_commands = ['@SP',  # SP -= 2;
                             'M=M-1',
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             '@SP',  # SP++;
                             'M=M+1',
                             'A=M',  # *SP = M-D
                             'M=M-D'
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_neg(self):
        """Translate negation arithmetic command"""
        assembly_commands = ['@SP',  # SP --;
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             'M=-D',  # *SP = -D
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_eq(self):
        """Translate '== or EQUAL' logical operation command"""
        assembly_commands = ['@SP',  # SP -= 2;
                             'M=M-1',
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             '@SP',  # SP++;
                             'M=M+1',
                             'A=M',  # *SP = M-D
                             'D=M-D',
                             '@EQUAL',
                             ''
                             '(EQUAL)'
                             '(NO_EQUAL)'
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_gt(self):
        """Translate '> or GREATER THAN' logical operation command"""
        pass

    def __translate_lt(self):
        """Translate ' < or LESS THAN' logical operation command"""
        pass

    def __translate_and(self):
        """Translate '&& or AND' logical operation command"""
        assembly_commands = ['@SP',  # SP -= 2;
                             'M=M-1',
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             '@SP',  # SP++;
                             'M=M+1',
                             'A=M',  # *SP = M&D
                             'M=M&D'
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_or(self):
        """Translate '|| or OR' logical operation command"""
        assembly_commands = ['@SP',  # SP -= 2;
                             'M=M-1',
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             '@SP',  # SP++;
                             'M=M+1',
                             'A=M',  # *SP = M|D
                             'M=M|D'
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_not(self):
        """Translate '! or NOT' logical operation command"""
        assembly_commands = ['@SP',  # SP --;
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M',
                             'M=!D',  # *SP = !D
                             '@SP',  # SP++;
                             'M=M+1'
                             ]

    def __translate_push_constant(self, index):
        """Translate push constant command"""
        assembly_commands = [f'@{index}',
                             'D=A',
                             '@SP',
                             'A=M',
                             'M=D',
                             '@SP',
                             ]

    def __translate_push_static(self, index):
        """Translate push static command"""
        assembly_command = [f'@{self.file_name}.{index}',  # D = RAM[filename.index]
                            'D=M',
                            '@SP',  # RAM[*SP]= D
                            'A=M',
                            'M=D',
                            '@SP',  # RAM[SP++]
                            'M=M+1',
                            ]

    def __translate_pop_static(self, index):
        """Translate pop static command"""
        assembly_command = ['@SP',  # D = *SP
                            'A=M-1',
                            'D=M'
                            f'@{self.file_name}.{index}',  # file_name.index = D
                            'M=D',
                            '@SP',  # RAM[SP++]
                            'M=M+1',
                            ]

    def __translate_push_pointer(self, binary):
        """Translate push pointer command"""
        assert binary == 0 or binary == 1
        this_or_that = 'THIS' if binary == 0 else 'THAT'
        assembly_commands = [f'@{this_or_that}',  # D = this_or_that
                             'D=A',
                             '@SP',  # *SP = D
                             'A=M',
                             'M=D',
                             '@SP',  # SP++
                             'M=M+1']

    def __translate_pop_pointer(self, binary):
        """Translate push pointer command"""
        assert binary == 0 or binary == 1
        this_or_that = 'THIS' if binary == 0 else 'THAT'
        assembly_commands = ['@SP',  # SP--
                             'M=M-1',
                             'A=M',  # D = *SP
                             'D=M'
                             f'@{this_or_that}',  # this_or_that = D
                             'M=D',
                             ]

    def __translate_push(self, segment, index):
        """Translates push command of LCL, ARG, THIS, THAT, temp segments"""
        assembly_commands = [f'@{segment_pointers[segment]}',  # D = RAM[seg + i]
                             f'D=M',
                             f'@{index}',
                             f'A=A+D',
                             'D=M',
                             '@SP',  # RAM[SP]= D
                             'A=M',
                             'M=D',
                             '@SP',  # SP++;
                             'M=M+1']
        return assembly_commands

    def __translate_pop(self, segment, index):
        """Translates pop command of LCL, ARG, THIS, THAT segments"""
        assembly_commands = [f'@{segment_pointers[segment]}',  # D = RAM[seg + i]
                             'D=M',
                             f'@{index}',
                             'D=A+D',
                             '@addr',
                             'M=D',
                             '@SP',  # SP--
                             'M=M-1',
                             'A=M',  # D= RAM[SP]
                             'D=M',
                             '@addr',  # RAM[addr] = D
                             'A=M',
                             'M=D',
                             ]

    def __push(self, segment, index):
        """ Handles push command"""
        if segment in segment_pointers:
            self.__translate_push(segment, index)

    def __pop(self, segment, index):
        """ Handles pop command"""
        print('POP>>>', segment, index)

    def write_push_pop(self, command, segment, index):
        """
            Writes to the output file the assembly code that implements
            the given command, where command is either C_PUSH or C_POP
        """
        assert command in [C_PUSH, C_POP]
        assert segment in MEMORY_SEGMENTS
        assert type(index) == int
        if command == C_PUSH:
            self.__push(segment, index)
        else:
            self.__pop(segment, index)

    def close(self):
        """Closes the input file"""
        if self.file:
            self.close()
