from parser import Parser, CommandType


def translate():
    """Translates file.vm commands into file.asm command"""
    with Parser('BasicTest.vm') as parser:
        for cursor in parser:
            if cursor.command_type() == CommandType.C_ARITHMETIC:
                print(cursor.command_type(), cursor.arg1())
            else:
                print(cursor.command_type(), cursor.arg1(), cursor.arg2())


if __name__ == '__main__':
    translate()