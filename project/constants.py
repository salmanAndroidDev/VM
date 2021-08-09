import enum

# memory segments
MEMORY_SEGMENTS = ['local', 'argument', 'this', 'that',
                   'constant', 'static', 'pointer', 'temp']

# Arithmetic operations
ARITHMETIC_OPERATIONS = ['add', 'sub', 'neg', 'eq', 'gt',
                         'lt', 'and', 'or', 'not']

# memory segment pointers
segment_pointers = {'local': 'LCL',
                    'argument': 'ARG',
                    'this': 'THIS',
                    'that': 'THAT',
                    }


class CommandType(enum.Enum):
    """Command type enum to simplify command names"""
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


C_PUSH = CommandType.C_PUSH
C_POP = CommandType.C_POP