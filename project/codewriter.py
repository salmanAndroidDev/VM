from constants import ARITHMETIC_OPERATIONS, MEMORY_SEGMENTS, segment_pointers, C_PUSH, C_POP
from exceptions import ConstantHasNoPOPError
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

    def __translate_add(self):
        """Translate addition arithmetic command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=M+D',
                                '@SP', 'A=M+1', 'M=D', '@SP', 'M=M+1', ])

    def __translate_sub(self):
        """Translate subtraction arithmetic command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=M-D', '@SP',
                                'A=M+1', 'M=D', '@SP', 'M=M+1'])

    def __translate_neg(self):
        """Translate negation arithmetic command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'A=M+1', 'M=-D', '@SP', 'M=M+1'])

    def __translate_eq(self):
        """Translate '== or EQUAL' logical operation command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=D-M',
                                '@SP', 'A=M+1', 'M=1', '@CONTINUE', 'D;JEQ', '@SP', 'A=M', 'M=0', '(CONTINUE)',
                                '@SP', 'M=M+1',
                                ])

    def __translate_gt(self):
        """Translate '> or GREATER THAN' logical operation command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=D-M',
                                'M=1', '@CONTINUE', 'D;JGT', '@SP', 'A=M+1', 'M=0', '(CONTINUE)', '@SP',
                                'M=M+1'])

    def __translate_lt(self):
        """Translate ' < or LESS THAN' logical operation command"""
        self.__asm_code.extend(
            ['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=D-M', 'M=1', '@CONTINUE',
             'D;JLT', '@SP', 'A=M+1', 'M=0', '(CONTINUE)', '@SP', 'M=M+1'])

    def __translate_and(self):
        """Translate '&& or AND' logical operation command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=M&D', '@SP', 'A=M+1',
                                'M=D', '@SP', 'M=M+1', ])

    def __translate_or(self):
        """Translate '|| or OR' logical operation command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M+1', 'A=M', 'D=M|D', '@SP',
                                'A=M+1', 'M=D', '@SP', 'M=M+1'])

    def __translate_not(self):
        """Translate '! or NOT' logical operation command"""
        self.__asm_code.extend(['@SP', 'M=M-1', 'A=M', 'D=M', 'D=!D', '@SP', 'A=M+1', 'M=D', '@SP', 'M=M+1'])

    def __translate_push_constant(self, index):
        """Translate push constant command"""
        self.__asm_code.extend([f'@{index}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

    def __translate_push_static(self, index):
        """Translate push static command"""
        self.__asm_code.extend([f'@{self.file_name}.{index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

    def __translate_pop_static(self, index):
        """Translate pop static command"""
        self.__asm_code.extend(['@SP', 'A=M-1', 'D=M', f'@{self.file_name}.{index}', 'M=D', '@SP', 'M=M+1'])

    def __translate_push_pointer(self, binary):
        """Translate push pointer command"""
        assert binary == 0 or binary == 1
        this_or_that = 'THIS' if binary == 0 else 'THAT'
        self.__asm_code.extend([f'@{this_or_that}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

    def __translate_pop_pointer(self, binary):
        """Translate push pointer command"""
        assert binary == 0 or binary == 1
        this_or_that = 'THIS' if binary == 0 else 'THAT'
        self.__asm_code.extend(['@SP', 'M=M-1', 'A=M', 'D=M', f'@{this_or_that}', 'M=D'])

    def __translate_push_temp(self, index):
        """Translate push command"""
        self.__asm_code.extend(['@5', 'D=A', f'@{index}', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

    def __translate_pop_temp(self, index):
        """Translate pop command"""
        self.__asm_code.extend(['@5', 'D=A', f'@{index}', 'D=A+D', '@addr', 'M=D', '@SP', 'M=M-1', 'A=M', 'D=M',
                                '@addr', 'A=M', 'M=D'])

    def __translate_push(self, segment, index):
        """Translates push command of LCL, ARG, THIS, THAT, temp segments"""
        self.__asm_code.extend([f'@{segment_pointers[segment]}', 'D=M', f'@{index}', 'A=A+D', 'D=M', '@SP',
                                'A=M', 'M=D', '@SP', 'M=M+1'])

    def __translate_pop(self, segment, index):
        """Translates pop command of LCL, ARG, THIS, THAT segments"""
        self.__asm_code.extend([f'@{segment_pointers[segment]}', 'D=M', f'@{index}', 'D=A+D', '@addr', 'M=D', '@SP',
                                'M=M-1', 'A=M', 'D=M', '@addr', 'A=M', 'M=D', ])

    def __push(self, segment, index):
        """ Handles push command"""
        if segment in segment_pointers:
            self.__translate_push(segment, index)
        else:
            if segment == 'constant':
                self.__translate_push_constant(index)
            elif segment == 'pointer':
                self.__translate_push_pointer()
            elif segment == 'static':
                self.__translate_push_static()
            elif segment == 'temp':
                self.__translate_push_temp(index)

    def __pop(self, segment, index):
        """ Handles pop command"""
        if segment in segment_pointers:
            self.__translate_pop(segment, index)
        else:
            if segment == 'constant':
                raise ConstantHasNoPOPError()
            elif segment == 'pointer':
                self.__translate_pop_pointer()
            elif segment == 'static':
                self.__translate_pop_static()
            elif segment == 'temp':
                self.__translate_pop_temp(index)

    def write_arithmetic(self, operation):
        """
            Writes to the output file the assembly code that implements
            the given arithmetic command
        """
        assert operation in ARITHMETIC_OPERATIONS
        self.__asm_code.append(f'//      {operation}')

        if operation == 'add':
            self.__translate_add()
        elif operation == 'sub':
            self.__translate_sub()
        elif operation == 'neg':
            self.__translate_neg()
        elif operation == 'eq':
            self.__translate_eq()
        elif operation == 'gt':
            self.__translate_gt()
        elif operation == 'lt':
            self.__translate_lt()
        elif operation == 'and':
            self.__translate_and()
        elif operation == 'or':
            self.__translate_or()
        elif operation == 'not':
            self.__translate_not()

    def write_push_pop(self, command, segment, index):
        """
            Writes to the output file the assembly code that implements
            the given command, where command is either C_PUSH or C_POP
        """
        assert command in [C_PUSH, C_POP]
        assert segment in MEMORY_SEGMENTS
        assert type(index) == int
        self.__asm_code.append(f'//      {command} {segment} {index}')
        if command == C_PUSH:
            self.__push(segment, index)
        elif command == C_POP:
            self.__pop(segment, index)

    def write_to_file(self):
        """Writes from __asm_code into file.asm"""
        for command in self.__asm_code:
            self.file.write(command + '\n')

    def close_file(self):
        """Closes the input file"""
        if self.file:
            self.file.close()
