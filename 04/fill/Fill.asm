// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Read KBD regsiter

// # of registers in screen memory map

@8192
D=A
@max
M=D

(LOOP)
	@KBD
	D=M
	@WHITEN
	D;JEQ
	
(DARKEN)
	@counter
	M=0
(DARKEN_WORD)	// darken screen
	@SCREEN
	D=A
	@counter
	D=D+M
	M=M+1
	A=D
	M=0
	M=!M
	
	@max
	D=M
	@counter
	D=D-M
	@LOOP
	D;JEQ
	
	// check if key is still pressed
	@KBD
	D=M
	@WHITEN
	D;JEQ

	@DARKEN_WORD
	0;JMP
	

(WHITEN)
	@counter
	M=0
(WHITEN_WORD)// whiten screen
	@SCREEN
	D=A
	@counter
	D=D+M
	M=M+1
	A=D
	M=0
	
	@max
	D=M
	@counter
	D=D-M
	@LOOP
	D;JEQ

	// check if key is still not pressed
	@KBD
	D=M
	@BLACKEN
	D;JNE

	@WHITEN_WORD
	0;JMP
