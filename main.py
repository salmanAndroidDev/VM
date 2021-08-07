from parser import Parser
from codewriter import CodeWriter
from constants import CommandType, C_PUSH, C_POP


def translate():
    """Translates file.vm commands into file.asm command"""

    code_writer = CodeWriter('code.asm')
    with Parser('BasicTest.vm') as parser:
        for cursor in parser:
            command = cursor.command_type()
            if command == CommandType.C_ARITHMETIC:
                code_writer.write_arithmetic(cursor.arg1())
            elif command in [C_PUSH, C_POP]:
                code_writer.write_push_pop(command, cursor.arg1(), cursor.arg2())
            else:
                raise AssertionError('Something went wrong')


if __name__ == '__main__':
    translate()
