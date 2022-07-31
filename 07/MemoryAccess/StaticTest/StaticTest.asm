// push constant 111
@111
D=A
@R0
A=M
M=D
@R0
M=M+1
// push constant 333
@333
D=A
@R0
A=M
M=D
@R0
M=M+1
// push constant 888
@888
D=A
@R0
A=M
M=D
@R0
M=M+1
// pop static 8
@StaticTest.8
D=A
// pop static 3
@StaticTest.3
D=A
// pop static 1
@StaticTest.1
D=A
// push static 3
@StaticTest.3
D=M
@R0
A=M
M=D
@R0
M=M+1
// push static 1
@StaticTest.1
D=M
@R0
A=M
M=D
@R0
M=M+1
// sub 
@0
A=M
A=A-1
D=M
A=A-1
M=M-D
@0
M=M-1
// push static 8
@StaticTest.8
D=M
@R0
A=M
M=D
@R0
M=M+1
// add 
@0
A=M
A=A-1
D=M
A=A-1
M=M+D
@0
M=M-1
(LOOP)
@LOOP
0;JMP