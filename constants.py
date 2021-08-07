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
                    'temp': 5,
                    }


def push_normal_segments(segment, i):
    seg = segment_pointers[segment]



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

"""
**** Pointer
@p;
A=M;
D=M;

Stack pointer starts at RAM[0]
Stack base address is RAM[256]

# the logic of Push constant 17
*SP = 17;
SP++;
    ==> assembly:
        @17; *
        D=A; *
        @SP; *
        A=M; *
        M=D; *
        @SP*
        M=M+1;

# local point LCL RAM[1]
    RAM[LCL + arg2] = SP--; *SP;
    addr = (LCL + arg2);
    SP--; *addr=*SP;

pop local i => addr = [LCL + i]; sp--; *addr=*sp
push local i => addr = [local + i]; *SP= *addr; sp++;


==> SP, LCL, ARG, THIS, THAT;
*********** constant
push constant i => *SP=i; SP++;
there is no pop for constant

*********** static
pop static 5 => @ file_name.5; M=D(5);
pop static 2 => @file_name.2; M=D(2);

*********** temp
push temp i => add = 5 + 1; *SP=*addr; SP++;
pop temp i =>  addr = 5 + i; SP--; **addr=*SP;

*********** pointer
push 0/1 i => *SP=This/That; SP++;
pop 0/1 i => SP--; This/That=*SP;
"""
