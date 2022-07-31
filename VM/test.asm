//push constant 42
@42
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 31
@31
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 19
@19
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
//push constant 50
@50
D=A
@R0
A=M
M=D
@R0
M=M+1
// eq 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE0
D;JEQ
D=0
@SET0
0;JMP
(TRUE0)
D=-1
(SET0)
@R0
A=M-1
M=D
// neg 
@R0
AM=M-1
M=-M
//push constant 42
@42
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
// eq 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE1
D;JEQ
D=0
@SET1
0;JMP
(TRUE1)
D=-1
(SET1)
@R0
A=M-1
M=D
(LOOP)
@LOOP
0;JMP