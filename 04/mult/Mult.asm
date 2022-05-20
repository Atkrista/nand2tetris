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
	

	// init one register to hold the product 
	@R2
	M=0
	
	// check if either of the args are zero
	// then skip to the end
	//@R0
	//D=M
	//@R1
	//D=D&M
	//@END
	//D;JEQ
	@R0
	D=M
	@END
	D;JEQ

	@R1
	D=M
	@END
	D;JEQ

	// We use R[1] as a counter
	@R1
	D=M
	@second
	M=D
(LOOP)	
	// use R[0] to repeatedly sum to product
	@R0
	D=M

	@R2
	M=D+M

	// decrement counter and check if we are done
	@second
	M=M-1
	D=M
	@LOOP
	D;JNE
	
(END)
	@END
	0;JMP
