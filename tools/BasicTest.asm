//      CommandType.C_PUSH constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_POP local 0
@LCL
D=M
@0
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_PUSH constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_PUSH constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_POP argument 2
@ARG
D=M
@2
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_POP argument 1
@ARG
D=M
@1
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_PUSH constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_POP this 6
@THIS
D=M
@6
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_PUSH constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_PUSH constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_POP that 5
@THAT
D=M
@5
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_POP that 2
@THAT
D=M
@2
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_PUSH constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_POP temp 6
@5
D=A
@6
D=A+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
//      CommandType.C_PUSH local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_PUSH that 5
@THAT
D=M
@5
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      add
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=M+D
@SP
A=M+1
M=D
@SP
M=M+1
//      CommandType.C_PUSH argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      sub
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=M-D
@SP
A=M+1
M=D
@SP
M=M+1
//      CommandType.C_PUSH this 6
@THIS
D=M
@6
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      CommandType.C_PUSH this 6
@THIS
D=M
@6
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      add
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=M+D
@SP
A=M+1
M=D
@SP
M=M+1
//      sub
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=M-D
@SP
A=M+1
M=D
@SP
M=M+1
//      CommandType.C_PUSH temp 6
@5
D=A
@6
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//      add
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=M+D
@SP
A=M+1
M=D
@SP
M=M+1
