//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 17
@17
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
//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 16
@16
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
//push constant 16
@16
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 17
@17
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
@TRUE2
D;JEQ
D=0
@SET2
0;JMP
(TRUE2)
D=-1
(SET2)
@R0
A=M-1
M=D
//push constant 892
@892
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1
// lt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE3
D;JLT
D=0
@SET3
0;JMP
(TRUE3)
D=-1
(SET3)
@R0
A=M-1
M=D
//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 892
@892
D=A
@R0
A=M
M=D
@R0
M=M+1
// lt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE4
D;JLT
D=0
@SET4
0;JMP
(TRUE4)
D=-1
(SET4)
@R0
A=M-1
M=D
//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1
// lt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE5
D;JLT
D=0
@SET5
0;JMP
(TRUE5)
D=-1
(SET5)
@R0
A=M-1
M=D
//push constant 32767
@32767
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1
// gt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE6
D;JGT
D=0
@SET6
0;JMP
(TRUE6)
D=-1
(SET6)
@R0
A=M-1
M=D
//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 32767
@32767
D=A
@R0
A=M
M=D
@R0
M=M+1
// gt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE7
D;JGT
D=0
@SET7
0;JMP
(TRUE7)
D=-1
(SET7)
@R0
A=M-1
M=D
//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1
//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1
// gt 
@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE8
D;JGT
D=0
@SET8
0;JMP
(TRUE8)
D=-1
(SET8)
@R0
A=M-1
M=D
//push constant 57
@57
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
//push constant 53
@53
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
//push constant 112
@112
D=A
@R0
A=M
M=D
@R0
M=M+1
// sub 
@R0
AM=M-1
D=M
@R0
A=M-1
M=M-D
// neg 
@R0
A=M-1
M=-M
// and 
@R0
AM=M-1
D=M
@R0
A=M-1
M=M&D
//push constant 82
@82
D=A
@R0
A=M
M=D
@R0
M=M+1
// or 
@R0
AM=M-1
D=M
@R0
A=M-1
M=M|D
// not 
@R0
A=M-1
M=!M
(LOOP)
@LOOP
0;JMP