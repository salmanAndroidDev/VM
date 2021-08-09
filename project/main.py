import sys
from parser import Parser
from codewriter import CodeWriter
from constants import CommandType, C_PUSH, C_POP


def translate(file_name):
    """Translates file.vm commands into file.asm command"""
    file_name = sys.argv[1].split('.')[0] + '.asm'
    code_writer = CodeWriter(file_name)
    with Parser('../tools/BasicTest.vm') as parser:
        for cursor in parser:
            command = cursor.command_type()
            if command == CommandType.C_ARITHMETIC:
                code_writer.write_arithmetic(cursor.arg1())
            elif command in [C_PUSH, C_POP]:
                code_writer.write_push_pop(command, cursor.arg1(), cursor.arg2())
            else:
                raise AssertionError('Something went wrong')
        code_writer.write_to_file()
    code_writer.close_file()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        translate(sys.argv[1])
    else:
        print("Please send a vm file as argument")
