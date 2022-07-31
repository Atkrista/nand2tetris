//push constant 7
@7
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 8
@8
D=A
@R0
A=M
M=D
@R0
M=M+1
// add 
@R0
AM=M-1
D=M
@R0
A=M-1
M=M+D
(LOOP)
@LOOP
0;JMP