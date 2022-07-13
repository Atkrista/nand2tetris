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

    // pointer to a word in screen-memory map
    @addr
    M=0

    // val is written to every word in map
    @val
    M=0

    // max is the address after the last word in mem map
    @KBD
    D=A
    @max
    M=D

(MAIN_LOOP)
    @KBD
    D=M
    @CLEAR_SCREEN
    D;JEQ
    @FILL_SCREEN
    0;JMP

(FILL_SCREEN)
    @val
    M=-1
    @FILL
    0;JMP

(CLEAR_SCREEN)
    @val
    M=0
    @FILL
    0;JMP

(FILL)
    @SCREEN
    D=A
    // addr now has base address of SCREEN
    @addr
    M=D

(FILL2)
    @val
    D=M
    @addr
    A=M
    M=D

    @addr
    MD=M+1

    @max
    D=M-D
    @MAIN_LOOP
    D;JEQ
    @FILL2
    0;JMP
