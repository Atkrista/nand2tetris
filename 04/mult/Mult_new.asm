// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

	// idx = R1
	// sum = 0

	// while(idx > 0) {
	//	sum += first
	//	idx -= 1
	//}
	//
	//	R2 = sum

	// Leave the original values untouched



	@sum
	M=0

	// check if either argument is zero
	@R0
	D=M
	@END
	D;JEQ

	@R1
	D=M
	@END
	D;JEQ

	// add R1 to sum R0 times
	@R0
	D=M
	@counter
	M=D

(LOOP)
	@R1
	D=M
	@sum
	M=M+D

	@counter
	MD=M-1
	@LOOP
	D;JGT

(END)
	@sum
	D=M
	@R2
	M=D

(INF_LOOP)
	@INF_LOOP
	0;JMP
